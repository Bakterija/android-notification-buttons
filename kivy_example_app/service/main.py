from time import sleep
from kivy.utils import platform
from kivy.core.audio import SoundLoader
from kivy.lib import osc
from noti_builder.noti_builder import Notification_Builder
try:
    from jnius import autoclass
except: pass

class M_Player:
    def intent_callback(self,intent,*arg):
        ## BroadcastReceiver callbacks are done on a different thread and can crash
        ## the service on unsafe tasks, setting strings is safe
        self.parent.queue = intent

    def __init__(self,parent):
        try:
            self.nBuilder = Notification_Builder()
            self.nBuilder.set_title('Stop')
            self.nBuilder.set_message('msg')
            self.nBuilder.set_ticker('Button example')
            ## 0. Displayed button name
            ## 1. icon integer available at https://developer.android.com/reference/android/R.drawable.html
            ## 2. callback
            ## action= android PendingIntent action, button name will be used if not provided
            self.nBuilder.Button('Play', 17301540 , self.intent_callback, action='Play')
            self.nBuilder.Button('Pause', 17301539 , self.intent_callback, action='Pause')
            self.nBuilder.build()

            self.parent = parent
            self.sound = None
            self.pauseTime = None
            self.state = 'stop'
            self.path = '/data/data/org.test.npexample/files/rain.ogg'
        except Exception as e: osc.sendMsg('/some_api', ['Mplayer exception '+str(e)], port=3002)

    def play(self):
        osc.sendMsg('/some_api', ['Play'], port=3002)
        try:
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
            self.nBuilder.set_title('Play')
            self.nBuilder.build()
        except Exception as e:
            osc.sendMsg('/some_api', [str(e)], port=3002)

    def pause(self):
        try:
            osc.sendMsg('/some_api', ['Pause'], port=3002)
            if self.sound == None:
                pass
            else:
                self.pauseTime = self.sound.get_pos()
                self.sound.stop()
            self.state = 'pause'
            self.nBuilder.set_title('Pause')
            self.nBuilder.build()
        except Exception as e: osc.sendMsg('/some_api', [str(e)], port=3002)

    def osc_callback(self,message,*args):
        try:
            if message[2] == 'Play':
                self.play()
            elif message[2] == 'Pause':
                self.pause()
        except Exception as e: osc.sendMsg('/some_api', [str(e)], port=3002)

class Service:
    def __init__(self):
        sleep(1)
        osc.init()
        oscid = osc.listen(ipAddr='127.0.0.1', port=3001)
        try:
            osc.sendMsg('/some_api', ['Init'], port=3002)
            self.mplayer = M_Player(self)
            osc.bind(oscid, self.mplayer.osc_callback, '/some_api')
            self.queue = ''

            while True:
                osc.readQueue(oscid)
                if self.queue != '':
                    self.mplayer.osc_callback(['','',self.queue])
                    self.queue = ''
                    sleep(.3)
        except Exception as e:
            osc.sendMsg('/some_api', ['Service crash '+str(e)], port=3002)

def main_loop():
    service = Service()

if __name__ == '__main__':
    main_loop()
