#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
from kivy.utils import platform
from kivy.core.audio import SoundLoader
from kivy.lib import osc
try:
    from android.broadcast import BroadcastReceiver
    from jnius import autoclass
    from plyer import notification
except: pass

def do_notify(mode='normal',title='Title',message='Message',ticker='Ticker'):
    from npy import notification_modified
    from plyer.utils import platform
    from plyer.compat import PY2
    title = str(title)
    message = str(message)
    ticker = str(ticker)

    if PY2:
        title = title.decode('utf8')
        message = message.decode('utf8')
    kwargs = {'title': title, 'message': message, 'ticker': ticker}

    ee = notification_modified.AndroidNotification()
    ee.notify(**kwargs)
    return ee

class M_Player:
    def __init__(self,parent):
        self.br = BroadcastReceiver(self.on_broadcast, actions=['com.example.app.ACTION_PLAY'])
        self.br.start()
        self.br2 = BroadcastReceiver(self.on_broadcast, actions=['com.example.app.ACTION_STOP'])
        self.br2.start()

        self.times = 0
        self.parent = parent
        self.sound = None
        self.pauseTime = None
        self.state = 'stop'
        self.path = '/data/data/org.test.npexample/files/rain.ogg'

    def on_broadcast(self, context, intent):
        action = intent.getAction()
        if action == 'com.example.app.ACTION_PLAY':
            self.parent.queue = 'Play'
        elif action == 'com.example.app.ACTION_STOP':
            self.parent.queue = 'Pause'

    def play(self):
        if self.sound == None:
            if self.pauseTime == None:
                self.sound = SoundLoader.load(self.path)
                if self.sound:
                    self.sound.play()
        else:
            self.sound.play()
            if self.state == 'pause':
                sleep(0.2)
                self.sound.seek(int(self.pauseTime))
        self.state = 'play'
        do_notify(title='Play')

    def pause(self):
        if self.sound == None:
            pass
        else:
            self.pauseTime = self.sound.get_pos()
            self.sound.stop()
        self.state = 'pause'
        do_notify(title='Pause')

    def osc_callback(self,message,*args):
        if message[2] == 'Play':
            self.play()
        elif message[2] == 'Pause':
            self.pause()

class Service:
    def __init__(self):
        self.queue = ''
        self.mplayer = M_Player(self)
        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=3001)
        osc.bind(oscid, self.mplayer.osc_callback, '/some_api')

        while True:
            osc.readQueue(oscid)
            if self.queue != '':
                self.mplayer.osc_callback(['','',self.queue])
                self.queue = ''
            sleep(.3)


def main_loop():
    service = Service()

if __name__ == '__main__':
    main_loop()
