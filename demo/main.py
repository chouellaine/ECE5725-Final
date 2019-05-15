from kivy.app import App
from kivy.graphics import Color, Rectangle
import home


class MainApp(App):
    def build(self):
        return(home.HomeWidget())


if __name__ == '__main__':
    MainApp().run()
