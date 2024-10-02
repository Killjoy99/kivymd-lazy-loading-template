import logging

from kivy.properties import StringProperty
from kivy.utils import platform
from kivymd.uix.screen import MDScreen

logger = logging.getLogger(__name__)


class CallingScreen(MDScreen):
    phone_number = StringProperty("0776471033")

    def on_enter(self):
        # You can handle permission check here as well
        pass

    def make_phone_call(self, phone_number):
        if platform == "android":
            from my_android.permissions import request_phone_permission
            from my_android.phone_call import initiate_phone_call

            if request_phone_permission():
                initiate_phone_call(phone_number=phone_number)
            else:
                logger.info("Requesting phone call permissions")
                # Register a callback or observe the permission result
                self.requesting_permission = True
                # Set a listener or handler for the permission result
        else:
            logger.info(phone_number)

    def on_permissions_granted(self):
        if self.requesting_permission:
            self.make_phone_call(self.phone_number)  # Retry the phone call
            self.requesting_permission = False
