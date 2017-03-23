from kivy.properties import (
    NumericProperty, BooleanProperty, StringProperty, ListProperty)
from .scrollview191 import ScrollView192
from kivy.uix.behaviors import ButtonBehavior
from .numpad import Numpad, ActivityNumpad
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.app import App


Builder.load_string('''

<NToggleButton>:
    size_hint: 1, None
    Button:
        size_hint_x: 0.7
        font_size: self.height * 0.5
        background_normal: root.btn_img
        background_down: root.btn_img
        text_size: self.width, None
        padding: cm(0.2), 0
        text: 'Toggle %s' % (root.name)
        on_release: root.on_release()
    Button:
        size_hint_x: 0.3
        font_size: self.height * 0.5
        background_normal: root.btn_img
        background_down: root.btn_img
        text: str(root.is_on)
        on_release: root.on_release()


<NInputButton>:
    size_hint: 1, None
    Button:
        size_hint_x: 0.7
        font_size: self.height * 0.5
        background_normal: root.btn_img
        background_down: root.btn_img
        text_size: self.width, None
        padding: cm(0.2), 0
        text: 'Set %s' % (root.name)
        on_release: root.on_release()
    Button:
        size_hint_x: 0.3
        font_size: self.height * 0.5
        background_normal: root.btn_img
        background_down: root.btn_img
        text: str(root.num)
        on_release: root.on_release()


<NActivityButton>:
    size_hint: 1, None
    Button:
        size_hint_x: 0.7
        font_size: self.height * 0.5
        background_normal: root.btn_img
        background_down: root.btn_img
        text_size: self.width, None
        padding: cm(0.2), 0
        text: 'Set %s' % (root.name)
        on_release: root.on_release()
    Button:
        size_hint_x: 0.3
        font_size: self.height * 0.5
        background_normal: root.btn_img
        background_down: root.btn_img
        text: str(root.val)
        on_release: root.on_release()


<NotiBuilderLayout>:
    bar_width: self.width * 0.03
    bar_color: col_blue
    bar_inactive_color: col_blue[0], col_blue[1], col_blue[2], 0.5

    GridLayout:
        size_hint: 1, None
        padding: root.width * 0.05, 0
        height: self.minimum_height
        cols: 1

        Widget:
            size_hint_y: None
            height: root.height * 0.01

        NInputButton:
            id: id_select
            height: root.height * 0.1
            name: 'id'
            num: 1

        Widget:
            size_hint_y: None
            height: root.height * 0.01

        NActivityButton:
            id: activity_select
            height: root.height * 0.1
            name: 'activity'

        Widget:
            size_hint_y: None
            height: root.height * 0.01

        NToggleButton:
            id: autocancel
            height: root.height * 0.1
            name: 'autocancel'

        Widget:
            size_hint_y: None
            height: root.height * 0.01

        NToggleButton:
            id: ongoing
            height: root.height * 0.1
            name: 'ongoing'

        Widget:
            size_hint_y: None
            height: root.height * 0.01

        NToggleButton:
            id: vibrate
            height: root.height * 0.1
            name: 'vibrate'

        Widget:
            size_hint_y: None
            height: root.height * 0.01

        NToggleButton:
            id: sound
            height: root.height * 0.1
            name: 'sound'

        Section:
            size_hint_y: None
            height: root.height * 0.07
            text: "Ticker input box"
        TextInput:
            id: ticker
            size_hint_y: None
            font_size: self.height * 0.2
            height: root.height * 0.2
            text: 'Default ticker'

        Section:
            size_hint_y: None
            height: root.height * 0.07
            text: "Title input box"
        TextInput:
            id: title
            size_hint_y: None
            font_size: self.height * 0.2
            height: root.height * 0.2
            text: 'Default title'

        Section:
            size_hint_y: None
            height: root.height * 0.07
            text: "Subtext input box"
        TextInput:
            id: subtext
            size_hint_y: None
            font_size: self.height * 0.2
            height: root.height * 0.2
            text: 'Default subtext'

        Section:
            size_hint_y: None
            height: root.height * 0.07
            text: "Message input box"
        TextInput:
            id: message
            size_hint_y: None
            font_size: self.height * 0.2
            height: root.height * 0.2
            text: 'Default message'
''')


class NToggleButton(BoxLayout):
    btn_img = StringProperty('images/blue_dark.png')
    is_on = BooleanProperty()
    name = StringProperty()

    def on_release(self):
        self.is_on = not self.is_on
        if self.is_on:
            self.btn_img = 'images/blue_dark.png'
        else:
            self.btn_img = 'images/dgrey.png'


class NInputButton(BoxLayout):
    btn_img = StringProperty('images/blue_dark.png')
    num = NumericProperty()
    name = StringProperty()
    popup = None

    def on_release(self):
        if not self.popup:
            self.popup = Popup(size_hint=(0.8, 0.6), title_color=(0, 0, 0, 1),
            background='', background_color=(0.2, 0.2, 0.2, 0.9))
            self.popup.title = 'Set Notification id'
            self.popup.content = Numpad()
            self.popup.content.callback = self.numpad_select_callback
        self.popup.open()

    def numpad_select_callback(self, new_num):
        self.num = int(new_num)
        self.popup.dismiss()


class NActivityButton(BoxLayout):
    btn_img = StringProperty('images/blue_dark.png')
    val = StringProperty('App')
    name = StringProperty()
    popup = None

    def on_release(self):
        if not self.popup:
            self.popup = Popup(size_hint=(0.8, 0.3), title_color=(0, 0, 0, 1),
            background='', background_color=(0.2, 0.2, 0.2, 0.9))
            self.popup.title = 'Set Notification activity'
            self.popup.content = ActivityNumpad()
            self.popup.content.callback = self.numpad_select_callback
        self.popup.open()

    def numpad_select_callback(self, new_num):
        if new_num == 1:
            self.val = 'App'
        else:
            self.val = 'Service'
        self.popup.dismiss()


class NotiBuilderLayout(ScrollView192):
    popup = None

    def on_touch_remove(self):
        kwargs = {
            'id': self.ids.id_select.num,
            'activity': self.ids.activity_select.val,
            'autocancel': self.ids.autocancel.is_on,
            'ongoing': self.ids.ongoing.is_on,
            'vibrate': self.ids.vibrate.is_on,
            'sound': self.ids.sound.is_on,
            'subtext': self.ids.subtext.text,
            'ticker': self.ids.ticker.text,
            'title': self.ids.title.text,
            'message': self.ids.message.text}
        app = App.get_running_app()
        app.remove_notification(**kwargs)

    def on_touch_accept(self):
        kwargs = {
            'id': self.ids.id_select.num,
            'activity': self.ids.activity_select.val,
            'autocancel': self.ids.autocancel.is_on,
            'ongoing': self.ids.ongoing.is_on,
            'vibrate': self.ids.vibrate.is_on,
            'sound': self.ids.sound.is_on,
            'subtext': self.ids.subtext.text,
            'ticker': self.ids.ticker.text,
            'title': self.ids.title.text,
            'message': self.ids.message.text}
        app = App.get_running_app()
        app.build_notification(**kwargs)
