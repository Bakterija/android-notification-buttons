from __future__ import print_function
from kivy.properties import (
    ObjectProperty, ListProperty, DictProperty, StringProperty)
from kivy.uix.boxlayout import BoxLayout
from .app_buttons import AppBlueButton
from kivy.logger import Logger
from kivy.lang import Builder


Builder.load_string('''
<ActivitieBox>:
    orientation: 'vertical'
    size_hint_y: None
    height: len(self.children) * app.bsize * 1.1
    spacing: app.bsize * 0.1
''')


class ActivitieViewClass(AppBlueButton):
    activity = StringProperty()
    name = StringProperty()

    def refresh_view_attrs(self, act_box, index, data):
        self.text = '%s %s...' % (data['name'], data['activity'][:25])


class ActivitieBox(BoxLayout):
    viewclass_class = ActivitieViewClass
    data = DictProperty()

    def on_data(self, instance, value):
        items = value.items()
        value = [{'name': str(k), 'activity': str(v)} for k, v in items]
        Logger.info('ActivitieBox: on_data: {}'.format(value))

        if self.viewclass_class:
            children_count = len(self.children)
            value_count = len(value)
            if children_count != value_count:
                if children_count < value_count:
                    for count in range(0, value_count - children_count):
                        self.add_widget(self.viewclass_class())
                else:
                    for count in range(0, children_count - value_count):
                        self.remove_widget(self.children[-1])

            if self.children:
                for i, child in enumerate(reversed(self.children)):
                    child.refresh_view_attrs(self, i, value[i])
