from kivy.uix.label import Label
from kivy.lang import Builder


Builder.load_string('''
<MultiLineLabel@Label>:
    size_hint_y: None
    text_size: self.width, None
    height: self.texture_size[1]
''')


class MultiLineLabel(Label):
    pass
