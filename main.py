import asyncio

from kivy.core.window import Window
from kivymd.app import MDApp

from libs.uix.root import Root


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "kivymd - Lazy Load"

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"

        self.theme_cls.theme_style = "Light"

    def build(self):
        # Don't change self.root to self.some_other_name
        # refer https://kivy.org/doc/stable/api-kivy.app.html#kivy.app.App.root
        self.root = Root()

        self.root.push("welcome")


if __name__ == "__main__":
    asyncio.run(MainApp().async_run())
