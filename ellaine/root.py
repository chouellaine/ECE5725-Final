
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
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
            # Color(0.882, 0.976, 0.988, 1.0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        stud, prof = analysis.analyze(
            'twinkstud.wav', 'twinkprof.wav')
        stud_sound = wave.open('twinkstud.wav')
        prof_sound = wave.open('twinkprof.wav')

        self.add_widget(
            border.BorderWidget(
                id="bottom",
                f=prof,
                audio=prof_sound,
                size_hint=(.9, .4),
                pos_hint={'center_x': .5, 'center_y': .3}))

        self.add_widget(
            border.BorderWidget(
                id="top",
                f=stud,
                audio=stud_sound,
                size_hint=(.9, .4),
                pos_hint={'center_x': .5, 'center_y': .75}))

        self.add_widget(
            Button(
                id="home",
                size_hint=(0.1, 0.06),
                pos_hint={'center_x': .1, 'center_y': .05},
                text="Back",
                background_normal='',
                background_color=[0.5, 0.5, 0.6, 0.7]
            )
        )

        quit = Button(
            id="quit",
            size_hint=(0.1, 0.06),
            pos_hint={'center_x': .9, 'center_y': .05},
            text="Quit",
            background_normal='',
            background_color=[0.5, 0.5, 0.6, 0.7]
        )

        quit.bind(on_release=self.quit_callback)

        self.add_widget(quit)

    def quit_callback(self, instance):
        quit()

    def update_rect(self, *kargs):
        self.rect.pos = self.pos
        self.rect.size = self.size
