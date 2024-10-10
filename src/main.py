import cProfile  # noqa: F401
import logging

from kivy.core.window import Window
from kivy.utils import platform
from kivymd.app import MDApp
from libs.uix.root import Root

logging.basicConfig(level=logging.INFO)


class EntweniLazyTemplate(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Entweni Booking"
        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"

    def build(self):
        if platform != "android":
            Window.size = (420, 840)

        self.root = Root()
        self.root.load_screen("welcome", preload=True)

        self.root.push("welcome")


if __name__ == "__main__":
    # Start the kivy application
    EntweniLazyTemplate().run()
