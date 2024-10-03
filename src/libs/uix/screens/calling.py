import logging

from kivy.properties import StringProperty
from kivy.utils import platform
from kivymd.uix.screen import MDScreen

logger = logging.getLogger(__name__)


class CallingScreen(MDScreen):
    phone_number = StringProperty("0776471033")

    def on_enter(self):
        # Check if the permission is already granted when entering the screen
        if platform == "android":
            from my_android.permissions import request_phone_permission

            if not request_phone_permission():
                logger.info("Requesting phone call permissions on entering the screen")

    def make_phone_call(self, phone_number):
        if platform == "android":
            from my_android.permissions import request_phone_permission
            from my_android.phone_call import initiate_phone_call

            if request_phone_permission():
                initiate_phone_call(phone_number=phone_number)
            else:
                logger.info("Requesting phone call permissions")
                self.requesting_permission = True
        else:
            logger.info(f"Dialing {phone_number} on a non-Android platform.")

    def on_permissions_granted(self):
        # Retry making the phone call if permissions were previously requested
        if self.requesting_permission:
            self.make_phone_call(self.phone_number)
            self.requesting_permission = False
