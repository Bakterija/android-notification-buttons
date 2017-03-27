from kivy.properties import BooleanProperty, ListProperty, DictProperty
from app_modules.simple_tcp.client import SimpleClient
from app_modules.noti_builder import NotificationBuilder
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.metrics import cm, dp
from kivy.utils import platform
from kivy.logger import Logger
from kivy.app import App
from time import sleep
from sys import path
import json
if platform == 'android':
    from android import AndroidService
    from jnius import autoclass
    import android


class NotificationDemo(FloatLayout):
    noti_ongoing = BooleanProperty()
    noti_autocancel = BooleanProperty()
    noti_subtext = BooleanProperty()

    def __init__(self, app, **kwargs):
        super(NotificationDemo, self).__init__( **kwargs)
        self.app = app

    def go_back(self):
        self.hide_back_btn()
        self.ids.sm.current = 'main'

    def show_back_btn(self):
        self.ids.back_btn.size = self.ids.tbar.height, self.ids.tbar.height
        self.ids.back_btn.opacity = 1.0
        self.ids.back_btn.disabled = False

    def hide_back_btn(self):
        self.ids.back_btn.size = 1, 1
        self.ids.back_btn.opacity = 0.0
        self.ids.back_btn.disabled = True


class NotificationDemoApp(App):
    connected = BooleanProperty(False)
    client = SimpleClient()
    nbuilder = NotificationBuilder()
    service = None

    def build(self):
        self.root = NotificationDemo(self)
        if platform == 'android':
            try:
                self.service = autoclass(
                    'org.test.npexample.ServiceMyservice')
                mActivity = autoclass(
                    'org.kivy.android.PythonActivity').mActivity
                argument = ''
                self.service.start(mActivity, argument)
            except:
                self.service = AndroidService(
                    'Sevice example', 'service is running')
                self.service.start('Hello From Service')
        else:
            Window.system_size = cm(7), cm(12)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        Clock.schedule_once(self.try_connecting, 0)
        Clock.schedule_interval(self.handle_msg, 0.1)
        # def skipp(*a):
        #     self.root.ids.sm.current = 'main'
        # Clock.schedule_once(skipp, 0.5)
        return self.root

    def try_connecting(self, *args):
        try:
            if not self.connected:
                self.client.connect()
        except Exception as e:
            Logger.info(
                'Connection to service failed with error: "{}", '
                'reconnecting'.format(e))
            Clock.schedule_once(self.try_connecting, 2)

    def on_connected(self, _, value):
        if not value:
            Logger.info('NotificationDemoApp: reconnecting')
            Clock.schedule_once(self.try_connecting, 0)

    def on_connect(self, *args):
        self.connected = True
        Logger.info('NotificationDemoApp: on_connect()')
        self.root.ids.sm.current = 'main'

    def on_disconnect(self, *args):
        self.connected = False
        Logger.info('NotificationDemoApp: on_disconnect()')

    def send_json(self, msg):
        self.send_msg(json.dumps(msg))

    def send_msg(self, msg):
        if self.connected:
            try:
                self.client.send(msg)
            except Exception as e:
                Logger.error('NotificationDemoApp: send_mesg: {}'.format(e))
                self.on_disconnect()

    def handle_msg(self, *args):
        if self.client:
            msg = self.client.read_queue()
            if msg:
                Logger.info('App: msg={}'.format(msg))

    def build_notification(self, **kwargs):
        if kwargs['activity'] == 'App':
            for k in (
                'id', 'ticker', 'subtext', 'message', 'ongoing', 'autocancel',
                'title'):
                self.nbuilder.kwargs[k] = kwargs[k]
            if kwargs['vibrate']:
                self.nbuilder.kwargs['vibrate'] = 1.0
            else:
                self.nbuilder.kwargs['vibrate'] = 0.0
            if kwargs['sound']:
                self.nbuilder.kwargs['sound'] = path[4] + '/audio/beep1.wav'
            else:
                self.nbuilder.kwargs['sound'] = ''
            self.nbuilder.build()

        else:
            msg = json.dumps(
                {'method': 'build_notification', 'kwargs': kwargs})
            Logger.info('build_notification: %s' % (msg))
            self.send_msg(msg)

    def remove_notification(self, **kwargs):
        if kwargs['activity'] == 'App':
            self.nbuilder.remove_notification(id=kwargs['id'])

        else:
            msg = json.dumps(
                {'method': 'remove_notification', 'kwargs': kwargs})
            self.send_msg(msg)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def stop_service(self):
        if platform == 'android':
            android.stop_service()

    def on_stop(self):
        self.nbuilder.remove_notification(id=11)
        if self.service:
            self.stop_service()


if __name__ == '__main__':
    app = NotificationDemoApp()
    app.run()
