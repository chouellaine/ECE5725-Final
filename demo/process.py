from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
import border
import home
import analysis
import analysis_async
import wave
import os


class ProcessWidget(FloatLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(ProcessWidget, self).__init__(**kwargs)
        with self.canvas:
            # Color(0.882, 0.976, 0.988, 1.0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        stud_file = kwargs.get("stud")
        prof_file = kwargs.get("prof")
        stud, prof = analysis_async.analyze(
            stud_file, prof_file)
        stud_sound = wave.open(stud_file)
        prof_sound = wave.open(prof_file)

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

        home = Button(
            id="home",
            size_hint=(0.1, 0.06),
            pos_hint={'center_x': .1, 'center_y': .05},
            text="Back",
            background_normal='',
            background_color=[0.5, 0.5, 0.6, 0.7]
        )

        self.add_widget(home)

        quit = Button(
            id="quit",
            size_hint=(0.1, 0.06),
            pos_hint={'center_x': .9, 'center_y': .05},
            text="Quit",
            background_normal='',
            background_color=[0.5, 0.5, 0.6, 0.7]
        )

        home.bind(on_release=self.home_page)
        quit.bind(on_release=self.quit_callback)

        self.add_widget(quit)

        cmap = Image(source='cmap.png', pos_hint={
            'center_x': .94, 'center_y': .53}, size_hint=(0.1, 0.7))

        self.add_widget(cmap)

        self.add_widget(Label(
            text="Soft",
            color=[0.0, 0.0, 0.0, 1.0],
            size_hint=(0.1, 0.1),
            pos_hint={'x': 0.89, 'center_y': 0.9}))

        self.add_widget(Label(
            text="Loud",
            color=[0.0, 0.0, 0.0, 1.0],
            size_hint=(0.1, 0.08),
            pos_hint={'x': 0.89, 'center_y': 0.15}))

        self.add_widget(Label(
            text="Student",
            color=[0.0, 0.0, 0.0, 1.0],
            size_hint=(0.1, 0.1),
            pos_hint={'x': 0.08, 'center_y': 0.96}))

        self.add_widget(Label(
            text="Professional",
            color=[0.0, 0.0, 0.0, 1.0],
            size_hint=(0.1, 0.1),
            pos_hint={'x': 0.1, 'center_y': 0.509}))

    def home_page(self, instance):
        self.add_widget(
            home.HomeWidget(
                id="home",
                size_hint=(1, 1),
                pos_hint={'center_x': .5, 'center_y': .5})
        )

    def quit_callback(self, instance):
        for file in os.listdir(os.getcwd()):
            if file.endswith(".pyc"):
                os.remove(file)
        quit()

    def update_rect(self, *kargs):
        self.rect.pos = self.pos
        self.rect.size = self.size
