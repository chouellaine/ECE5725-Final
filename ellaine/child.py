from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
import note
import wave


class ChildWidget(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(ChildWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(.890, 0.870, 0.949, 1.0)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.audio = kwargs.get("audio")
        self.audio_len = self.audio.getnframes()/self.audio.getframerate()
        self.blocks = int(round(self.audio_len/(0.15)))
        self.curr_block = 1
        _, _, _, p = zip(*(kwargs.get("f")))
        print(repr(p))
        self.max_freq = max(p)
        self.init_notes(kwargs.get("f"))
        self.show_notes()

    """
    [update_rect] updates the positioning of the rectangle that gives this
    widget its background color when the widget size has been changed.
    """

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def map_time(self, t):
        return round((t/self.get_audio_len()), 2)

    """
    [map_coord] converts information from analysis.py into the appropriate
        Note information
    """

    def map_coord(self, t_start, t_end, p):
        x_l = self.map_time(t_start)
        x_r = self.map_time(t_end)
        x_c = round((x_r + x_l)/2, 2)
        x_len = round(x_r - x_l)
        y_c = round((p/self.get_maxf()), 2)
        return x_c, x_len, y_c

    """
    [init_notes] initalizes a Note for each detected note from analysis.py
    and adds it to the parent widget
    """

    def init_notes(self, f):
        end_time = self.get_audio_len()
        main_x = self.size[0]
        for n in f:
            x_c, x_len, y_c = self.map_coord(n[0], n[1], n[3])
            self.add_widget(
                note.Note(
                    start=n[0],
                    end=n[1],
                    background_color=n[2],
                    text="",
                    size_hint=(x_len, .1),
                    pos_hint={'center_x': x_c, 'center_y': y_c}),
                index=0)
    """
    [show_notes] shows all the notes within the time span of [self.block]
    """

    def show_notes(self):
        min_time = self.get_block() * 0.15
        max_time = (self.get_block() + 1) * 0.15
        for widget in self.walk(restrict=True):
            if (type(widget)is note.Note):
                if (type(widget) is note.Note) and min_time <= widget.get_end() and widget.get_end() <= max_time and min_time <= widget.get_start() and widget.get_start() <= max_time:
                    widget.set_visible(1)
                else:
                    widget.set_visible(0)

                widget.toggleVisible()

    def get_block(self):
        return self.curr_block

    def get_maxf(self):
        return self.max_freq

    def get_audio_len(self):
        return self.audio_len

    def set_block(self, n):
        return
