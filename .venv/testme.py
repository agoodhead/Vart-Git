import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class MyW(GridLayout):
    pass

class e8App(App):
    def build(self):
        return MyW()

if __name__ == '__main__':
    e8App().run()