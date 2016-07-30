import kivy
from kivy.lib import osc
from kivy.clock import Clock, mainthread
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from plyer.utils import platform
from kivy.uix.label import Label
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

class NotificationDemo(BoxLayout):

    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__( **kwargs)
        self.scroller = self.children[-1]

        self.grid = GridLayout(cols=1, spacing=1, size_hint_y=None)
        self.scroller.add_widget(self.grid)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=3002)
        osc.bind(oscid, self.add_more, '/some_api')
        Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0.3)

    def add_more(self,message,*args):
        Label = MultiLineLabel(text=message[2])
        self.grid.add_widget(Label)

    def play(self):
        osc.sendMsg('/some_api', ['Play'], port=3001)

    def pause(self):
        osc.sendMsg('/some_api', ['Pause'], port=3001)

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
        return True
        
    def on_resume(self):
        pass

if __name__ == '__main__':
    NotificationDemoApp().run()
