from kivy.properties import NumericProperty
from jnius import autoclass
AndroidMediaPlayer = autoclass('android.media.MediaPlayer')


class MediaPlayer(object):
    '''Native android media player'''
    pause_time = 0.0
    sound = None
    state = 'stop'
    enabled = False

    def __init__(self, mpath, on_play=None, on_pause=None):
        self.mpath = mpath
        if on_play:
            self.on_play = on_play
        if on_pause:
            self.on_pause = on_pause

    def load(self, path):
        try:
            self.sound = AndroidMediaPlayer()
            self.sound.setDataSource(path)
            self.state = 'stop'
            self.sound.prepare()
            self.length = self.sound.getDuration() / 1000
            self.enabled = True
        except Exception as e:
            print('MediaPlayer: load:', e)

    def play(self, *arg):
        if not self.sound:
            self.load(self.mpath)
        if self.enabled:
            self.state = 'play'
            self.sound.start()
            self.on_play()

    def pause(self, *arg):
        if self.enabled:
            self.pause_time = self.sound.getCurrentPosition()
            self.sound.pause()
            self.state = 'pause'
            self.on_pause()

    def on_play(self):
        # Stub method that is called when state is set to 'play'
        pass

    def on_pause(self):
        # Stub method that is called when state is set to 'pause'
        pass
