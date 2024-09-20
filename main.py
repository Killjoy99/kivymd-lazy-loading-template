import cProfile  # noqa: F401
import logging

from kivy.core.window import Window
from kivy.utils import platform
from kivymd.app import MDApp

# Import the optimized Root class
# from libs.uix.optimised_root import Root
from libs.uix.root import Root

logging.basicConfig(level=logging.INFO)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "kivymd - Lazy Load"
        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "A500"
        self.theme_cls.accent_hue = "A100"

    def build(self):
        # Set window size only if running on non-Android platforms

        if platform != "android":
            Window.size = (420, 840)

        # Initialize the root widget
        self.root = Root()
        self.root.push("welcome")


if __name__ == "__main__":
    MainApp().run()
