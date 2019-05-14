from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
import child


class BorderWidget(FloatLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(BorderWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(0.5, 0.5, 0.5, 1.0)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

        f = kwargs.get("f")
        audio = kwargs.get("audio")

        self.add_widget(
            child.ChildWidget(
                f=f,
                audio=audio,
                size_hint=(.9, .8),
                pos_hint={'center_x': .5, 'center_y': .5}))

    def update_rect(self, *kargs):
        self.rect.pos = self.pos
        self.rect.size = self.size
