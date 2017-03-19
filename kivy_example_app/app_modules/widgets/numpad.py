from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder


Builder.load_string('''
<NumpadBlueButton@BlueButton>:
    on_release: self.parent.select_btn(self.text)


<Numpad>:
    cols: 3
    rows: 4
    spacing: 3, 3
    NumpadBlueButton:
        text: '1'
    NumpadBlueButton:
        text: '2'
    NumpadBlueButton:
        text: '3'
    NumpadBlueButton:
        text: '4'
    NumpadBlueButton:
        text: '5'
    NumpadBlueButton:
        text: '6'
    NumpadBlueButton:
        text: '7'
    NumpadBlueButton:
        text: '8'
    NumpadBlueButton:
        text: '9'


<ActivityNumpad>:
    cols: 1
    rows: 2
    spacing: 3, 3
    BoxLayout:
        size_hint_y: 0.5
        orientation: 'horizontal'
        BlueButton:
            size_hint: 0.2, 1
            text: '1'
            on_release: root.select_btn(1)
        BlueButton:
            size_hint: 0.8, 1
            text: 'App'
            on_release: root.select_btn(1)

    BoxLayout:
        size_hint_y: 0.5
        orientation: 'horizontal'
        BlueButton:
            size_hint: 0.2, 1
            text: '2'
            on_release: root.select_btn(2)
        BlueButton:
            size_hint: 0.8, 1
            text: 'Service'
            on_release: root.select_btn(2)
''')


class Numpad(GridLayout):
    selected_btn = 1
    callback = None

    def select_btn(self, num):
        self.selected_btn = num
        if self.callback:
            self.callback(num)


class ActivityNumpad(GridLayout):
    selected_btn = 1
    callback = None

    def select_btn(self, num):
        self.selected_btn = num
        if self.callback:
            self.callback(num)
