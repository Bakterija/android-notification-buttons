from plyer.utils import platform
from plyer.compat import PY2
from kivy.logger import Logger
if platform == 'android':
    from android.broadcast import BroadcastReceiver
    from . import notification
else:
    notification = None
    Logger.warning(
        'Platform is not android, ignoring AndroidNotification and '
        'BroadcastReceiver imports')


class Receiver(object):
    def __init__(self):
        self.registered = False
        self.intentName = ''
        self.actionName = ''

    def register(self, intentName, actionName, callback):
        self.br = BroadcastReceiver(
            self.on_broadcast, actions=[intentName+actionName])
        self.intentName = intentName
        self.actionName = actionName
        self.callback = callback
        self.registered = True

    def stop(self):
        if self.registered:
            self.br.stop()

    def start(self):
        if self.registered:
            self.br.start()

    def on_broadcast(self, context, intent):
        actionName = self.actionName
        action = intent.getAction()
        if self.intentName + actionName == action:
            self.callback(actionName)


class NotificationBuilder(object):
    def __init__(self, id=1):
        if notification:
            self.AndroidNotification, self.javaBuilder = self.get_builder()
        self.buttons = []
        self.receivers = []
        self.kwargs = {
            'title': 'Title',
            'message': 'Message',
            'ticker': 'Ticker',
            'subtext': None,
            'buttons': self.buttons,
            'intentName': 'org.renpy.android.ACTION_',
            'ongoing': False,
            'autocancel': False,
            'vibrate': None,
            'sound': '',
            'id': id
            }

    def get_builder(self):
        android_noti = notification.AndroidNotification()
        android_noti_builder = android_noti.noti
        return android_noti, android_noti_builder

    def get_receivers(self):
        return self.receivers

    def set_id(self, number):
        self.kwargs['id'] = number

    def set_title(self, string):
        self.kwargs['title'] = string

    def set_message(self, string):
        self.kwargs['message'] = string

    def set_ticker(self, string):
        self.kwargs['ticker'] = string

    def set_subtext(self, string):
        self.kwargs['subtext'] = string

    def set_intent(self, string):
        self.kwargs['intentName'] = string

    def set_ongoing(self, boolean):
        self.kwargs['ongoing'] = boolean

    def set_autocancel(self, boolean):
        self.kwargs['autocancel'] = boolean

    def set_vibrate(self, flt):
        self.kwargs['vibrate'] = flt

    def set_sound(self, string):
        self.kwargs['sound'] = string

    def set_intentName(self, string):
        self.kwargs['intentName'] = string

    def add_button(self, name, icon, callback, action=None):
        self.add_button_func(name, icon, callback, action)

    def Button(self, name, icon, callback, action=None):
        self.add_button_func(name, icon, callback, action)

    def add_button_func(self, name, icon, callback, action):
        ## 0. Displayed button name
        ## 1. icon integer available at https://developer.android.com/reference/android/R.drawable.html
        ## 2. callback
        ## action= android PendingIntent action, button name will be used if not provided
        if action == None:
            action = name
        self.buttons.append([action,name,icon,callback])
        self.buttonChange = True

    def remove_button(self, bName):
        found = False
        for i,x in iterate(self.buttons):
            if x[1] == bName:
                delvar = i
                found = True
                break
        if found:
            for i2,x in iterate(self.receivers):
                if x.actionName == self.buttons[i][0]:
                    x.stop()
                    del self.receivers[i2]
                    break
            del self.buttons[i]

    def remove_buttons(self):
        self.buttons = []
        self.stop()
        self.receivers = []

    def stop(self):
        for x in self.receivers:
            x.stop()

    def start(self):
        for x in self.receivers:
            x.start()

    def remove_notification(self, id=0):
        ee = notification.AndroidNotification()
        ee.remove(id)

    def build(self):
        if PY2:
            self.kwargs['title'] = self.kwargs['title'].decode('utf8')
            self.kwargs['message'] = self.kwargs['message'].decode('utf8')
            self.kwargs['ticker'] = self.kwargs['ticker'].decode('utf8')
            self.kwargs['ticker'] = self.kwargs['ticker'].decode('utf8')

        self.AndroidNotification.notify(**self.kwargs)
        self.AndroidNotification, self.javaBuilder = self.get_builder()

        if self.buttons != [] and self.buttonChange:
            for action,name,icon,callback in self.buttons:
                found = False
                for x in self.receivers:
                    if x.actionName == action:
                        found = True
                        break
                if not found:
                    receiver = Receiver()
                    receiver.register(self.kwargs['intentName'], action, callback)
                    self.receivers.append(receiver)
            self.start()
        self.buttonChange = False
