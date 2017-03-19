from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty


class AppScreenManager(ScreenManager):
    root_widget = ObjectProperty

    def switch_to(self, screen, **options):
        self.current = screen
        self.root_widget.show_back_btn()
