import kivy
from kivy.lib import osc
from kivy.clock import Clock, mainthread
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.utils import platform
kivy.require('1.8.0')

class MultiLineLabel(Label):
    def __init__(self, **kwargs):
        super(MultiLineLabel, self).__init__( **kwargs)
        self.markup = True
        self.text_size = self.size
        self.bind(size= self.on_size)
        self.bind(text= self.on_text_changed)
        self.size_hint_y = None # Not needed here

    def on_size(self, widget, size):
        self.text_size = size[0], None
        self.texture_update()
        if self.size_hint_y == None and self.size_hint_x != None:
            self.height = max(self.texture_size[1], self.line_height)
        elif self.size_hint_x == None and self.size_hint_y != None:
            self.width  = self.texture_size[0]

    def on_text_changed(self, widget, text):
        self.on_size(self, self.size)

class NotificationDemo(StackLayout):

    def __init__(self, **kwargs):
        super(StackLayout, self).__init__( **kwargs)
        self.scroller = self.children[-1]

        self.grid = GridLayout(cols=1, spacing=1, size_hint_y=None)
        self.scroller.add_widget(self.grid)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=3002)
        osc.bind(oscid, self.osc_callback, '/some_api')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0.3)

    def osc_callback(self,message,*args):
        msg = message[2]
        Label = MultiLineLabel(text=message[2])
        self.grid.add_widget(Label)

        ongoingbtn = self.children[-3]
        autocancelbtn = self.children[-4]
        subtextbtn = self.children[-5]
        oncolor = (0.4,0.5,0.75,1)
        off_color = (0.5,0.5,0.5,1)
        if msg == 'ongoing1':
            ongoingbtn.background_color = oncolor
        elif msg == 'ongoing0':
            ongoingbtn.background_color = off_color

        elif msg == 'autocancel1':
            autocancelbtn.background_color = oncolor
        elif msg == 'autocancel0':
            autocancelbtn.background_color = off_color

        elif msg == 'subtext1':
            subtextbtn.background_color = oncolor
        elif msg == 'subtext0':
            subtextbtn.background_color = off_color

    def play(self):
        osc.sendMsg('/some_api', ['Play'], port=3001)

    def pause(self):
        osc.sendMsg('/some_api', ['Pause'], port=3001)

    def remove_notification(self):
        osc.sendMsg('/some_api', ['Remove_noti'], port=3001)

    def toggle_ongoing(self):
        osc.sendMsg('/some_api', ['Toggle_ongoing'], port=3001)

    def toggle_autocancel(self):
        osc.sendMsg('/some_api', ['Toggle_autocancel'], port=3001)

    def toggle_subtext(self):
        osc.sendMsg('/some_api', ['Toggle_subtext'], port=3001)

    def quit(self):
        global service
        service.stop()


class NotificationDemoApp(App):
    def build(self):
        global service
        if platform == 'android':
            from android import AndroidService
            service = AndroidService('my service', 'running')
            service.start('service started')

        return NotificationDemo()

    def on_pause(self):
        osc.sendMsg('/some_api', ['Ping'], port=3001)
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    NotificationDemoApp().run()
