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
        # Set window size only if running on non-Android platforms
        if platform != "android":
            Window.size = (420, 840)

        self.root = Root()  # NOTE: Do not change this to self.anything_else
        # preload the welcome screen on app startup
        self.root.preload_screens(["welcome"])

    def on_start(self):
        if platform == "android":
            from my_android.permissions import request_camera_permission

            # Ensure the UI is drawn before requesting permissions
            Window.bind(on_draw=lambda *args: request_camera_permission())

        self.root.push("welcome")


if __name__ == "__main__":
    # Start the kivy application
    EntweniLazyTemplate().run()
