from kivy.app import App
from kivy.graphics import Color, Rectangle
import root


class MainApp(App):
    def build(self):
        return(root.RootWidget())
        """
        self.root = root = root.RootWidget()
        root.bind(size=self._update_rect, pos=self._update_rect)
        with root.canvas.before:
            Color(0.0, 0.0, 0.0, 0.5)  # colors range from 0-1 not 0-255
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size"""


if __name__ == '__main__':
    MainApp().run()
