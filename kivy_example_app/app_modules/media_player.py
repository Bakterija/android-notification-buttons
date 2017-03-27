from kivy.core.audio import SoundLoader


class MediaPlayer(object):
    pause_time = 0.0
    sound = None
    state = 'stop'

    def __init__(self, mpath, on_play=None, on_pause=None):
        self.mpath = mpath
        if on_play:
            self.on_play = on_play
        if on_pause:
            self.on_pause = on_pause

    def play(self):
        if not self.sound:
            self.sound = SoundLoader.load(self.mpath)
            if self.sound:
                self.sound.play()
        else:
            self.sound.play()
            self.sound.seek(self.pause_time)
        self.state = 'play'
        self.on_play()

    def pause(self):
        if not self.sound:
            return

        self.pause_time = self.sound.get_pos()
        self.sound.stop()
        self.state = 'pause'
        self.on_pause()

    def on_play(self):
        # Stub method that is called when state is set to 'play'
        pass

    def on_pause(self):
        # Stub method that is called when state is set to 'pause'
        pass
