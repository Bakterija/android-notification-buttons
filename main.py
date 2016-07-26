import kivy
from kivy.lib import osc
from kivy.clock import Clock, mainthread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from plyer.utils import platform
kivy.require('1.8.0')

class NotificationDemo(BoxLayout):

    def play(self):
        global osc
        osc.sendMsg('/some_api', ['Play'], port=3001)

    def pause(self):
        global osc
        osc.sendMsg('/some_api', ['Pause'], port=3001)

    def quit(self):
        global service
        service.stop()

def some_api_callback(message, *args):
    pass

class NotificationDemoApp(App):
    def build(self):
        if platform == 'android':
            from android import AndroidService
            global osc, service
            service = AndroidService('my service', 'running')
            service.start('service started')

            osc.init()
            oscid = osc.listen(ipAddr='127.0.0.1', port=3002)
            osc.bind(oscid, some_api_callback, '/some_api')
            Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0.1)
            return NotificationDemo()

        else:
            print('Not an android')

    def on_pause(self):
        return True
    def on_resume(self):
        pass

if __name__ == '__main__':
    NotificationDemoApp().run()
