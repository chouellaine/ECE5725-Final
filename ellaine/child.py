from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
import note
import wave

BLOCK_LEN = 15


class ChildWidget(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(ChildWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(0, 0, 0, 1.0)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)
        self.audio = kwargs.get("audio")
        self.audio_len = self.audio.getnframes()/self.audio.getframerate()
        # Number of BLOCK_LEN sec blocks
        if self.audio_len <= BLOCK_LEN:
            self.blocks = 0
        else:
            self.blocks = int(round(self.audio_len/(BLOCK_LEN)))
            if self.audio_len % BLOCK_LEN > 0:
                self.blocks += 1

        self.curr_block = 0
        _, _, _, p = zip(*(kwargs.get("f")))
        self.max_freq = max(p)
        print("max freq" + str(max(p)))
        self.init_notes(kwargs.get("f"))
        self.show_notes()

        init_t = Button(
            id="start",
            background_normal='',
            background_color=[0, 0, 0, 1],
            text=self.setTime(0),
            size_hint=(0.05, .01),
            pos_hint={'center_x': 0.05, 'center_y': 0.06}
        )
        final_t = Button(
            id="end",
            background_normal='',
            background_color=[0, 0, 0, 1],
            text=self.setTime(BLOCK_LEN),
            size_hint=(0.05, .01),
            pos_hint={'center_x': 0.95, 'center_y': 0.06}
        )
        self.add_widget(init_t)
        self.add_widget(final_t)

    """
    [update_rect] updates the positioning of the rectangle that gives this
    widget its background color when the widget size has been changed.
    """

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def map_time(self, t):
        factor = int(t / BLOCK_LEN)
        print("factor:" + str(factor))
        print("t: " + str(t))
        max = BLOCK_LEN * (factor + 1)
        return (t/max)

    """
    [map_coord] converts information from analysis.py into the appropriate
        Note information
    """

    def map_coord(self, t_start, t_end, p):
        print("freq: " + str(p))
        x_l = self.map_time(t_start)
        x_len = self.map_time(t_end)
        y = round(p/self.get_maxf(), 4)
        y = y - 0.2  # top margin
        print("y_len: "+repr(y))
        return x_l, x_len, y

    """
    [init_notes] initalizes a Note for each detected note from analysis.py
    and adds it to the parent widget
    """

    def init_notes(self, f):
        # print(repr(f))
        i = 0
        pad = 0.1
        for n in f:
            x_l, x_len, y = self.map_coord(n[0], n[1], n[3])
            x_l = x_l + i
            x_len = x_len/10
            n = note.Note(
                start=n[0],
                end=n[0]+n[1],
                background_normal='',
                background_color=n[2],
                text='',
                size_hint=(x_len, .1),
                pos_hint={'x': x_l, 'y': y})

            n.set_color(0)
            self.add_widget(n, index=0)
            i = x_len

    """
    [show_notes] shows all the notes within the time span of [self.block]
    """

    def show_notes(self):
        min_time = self.get_curr_block() * BLOCK_LEN
        max_time = (self.get_curr_block() + 1) * BLOCK_LEN
        # print("min: " + str(min_time))
        # print("max: " + str(max_time))
        for widget in self.walk(restrict=True):
            if (type(widget)is note.Note):
                if min_time <= widget.get_end()and widget.get_end() <= max_time and min_time <= widget.get_start()and widget.get_start() <= max_time:
                    # print("start: "+str(widget.get_start()))
                    # print("end: "+str(widget.get_end()))
                    # print("coord: "+repr(widget.pos_hint))
                    # print("len: "+repr(widget.size_hint))
                    widget.set_color(widget.get_alpha())
                else:
                    widget.set_color(0)

            elif (type(widget) is Button):
                if widget.id == "start":
                    widget.text = self.setTime(min_time)
                elif widget.id == "end":
                    widget.text = self.setTime(max_time)

    def get_curr_block(self):
        return self.curr_block

    def get_max_block(self):
        return self.blocks

    def get_maxf(self):
        return self.max_freq

    def get_audio_len(self):
        return self.audio_len

    """ if d = 1 then left button was pressed, if d = 0 then right button was pressed """

    def set_block(self, d):
        if d and self.get_curr_block() > 0:
            self.curr_block -= 1
            self.show_notes()
        elif not d and self.get_curr_block() < self.get_max_block():
            self.curr_block += 1
            self.show_notes()

    """ Convert time in seconds to minutes in the format of x:yz"""

    def setTime(self, t):
        if t < 10:
            return "0:0"+str(t)
        elif t < 60:
            return "0:"+str(t)
        else:
            m = t/60
            s = 60 % t
            if s == 0:
                return str(m)+":00"
            elif s < 10:
                return str(m) + ":0"+str(s)
            else:
                return str(m)+":"+str(s)
