from kivy.uix.button import Button


class Note(Button):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(Note, self).__init__(**kwargs)
        self.start = kwargs.get("start")
        self.end = kwargs.get("end")
        self.id = kwargs.get("id")
        self.alpha = self.background_color[-1]
        self.visible = 0

    def toggleVisible(self):
        if self.visible == 0:
            self.set_color(self.get_alpha())
            self.set_visible(1)
        else:
            self.set_color(0)
            self.set_visible(0)

    def get_alpha(self):
        return self.alpha

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def set_visible(self, x):
        self.visible = x

    def set_color(self, a):
        self.background_color = self.background_color[:3] + [a]
