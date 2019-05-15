from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
import child


class BorderWidget(FloatLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(BorderWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)
            #Color(0.5, 0.5, 0.5, 1.0)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

        f = kwargs.get("f")
        audio = kwargs.get("audio")

        main = child.ChildWidget(
            f=f,
            audio=audio,
            size_hint=(.9, .8),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        left = Button(
            id="left",
            text="<",
            size_hint=(.03, .06),
            pos_hint={'center_x': .85, 'center_y': .05}
        )
        right = Button(
            id="right",
            text=">",
            size_hint=(.03, .06),
            pos_hint={'center_x': .9, 'center_y': .05}
        )
        self.add_widget(main)
        self.add_widget(left)
        self.add_widget(right)
        left.bind(on_release=lambda x: self.shift_callback(1))
        right.bind(on_release=lambda x: self.shift_callback(0))

    def update_rect(self, *kargs):
        self.rect.pos = self.pos
        self.rect.size = self.size

    """Left and Right Button Callback: 
    if d = 1 then left button was pressed, 
    if d = 0 then right button was pressed."""

    def shift_callback(self, d):
        for widget in self.walk(restrict=True):
            if (type(widget)is child.ChildWidget):
                widget.set_block(d)
