from kivy.app import App
from kivy.lang import Builder

kv = """
BoxLayout:
    Label:
        text: 'Hello World'
"""


class MainApp(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    MainApp().run()
