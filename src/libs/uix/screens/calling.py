import logging

from kivy.clock import Clock
from kivy.utils import platform
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

logger = logging.getLogger(__name__)


class CallingScreen(MDScreen):
    phone_number = StringProperty("0776471033")  # Kivy's StringProperty handles the type

    def on_enter(self):
        # Potentially check for permissions
        pass

    def make_call(self, phone_number):
        if platform == "android":
            from my_android.phone_call import make_phone_call

            make_phone_call(phone_number=phone_number)

