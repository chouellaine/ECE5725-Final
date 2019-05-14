from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
import border
import analysis
import wave


class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
        with self.canvas:
            #Color(0.882, 0.976, 0.988, 1.0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        stud, prof = analysis.analyze(
            'test2.wav', 'test2.wav')
        stud_sound = wave.open('test2.wav')
        prof_sound = wave.open('test2.wav')

        self.add_widget(
            border.BorderWidget(
                id="bottom",
                f=prof,
                audio=prof_sound,
                size_hint=(.9, .4),
                pos_hint={'center_x': .5, 'center_y': .25}))

        self.add_widget(
            border.BorderWidget(
                id="top",
                f=stud,
                audio=stud_sound,
                size_hint=(.9, .4),
                pos_hint={'center_x': .5, 'center_y': .75}))

    def update_rect(self, *kargs):
        self.rect.pos = self.pos
        self.rect.size = self.size
