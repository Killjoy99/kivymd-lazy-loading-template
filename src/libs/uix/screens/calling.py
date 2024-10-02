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

    def make_phone_call(self, phone_number):
        if platform == "android":
            from my_android.phone_call import initiate_phone_call
            from my_android.permissions import request_phone_permission, PackageManager

            if request_phone_permission():
                initiate_phone_call(phone_number=phone_number)
            else:
                logging.info("Requesting phone call permissions")
                # Register a callback to re-attempt the call if permissions are granted
                def permission_callback(request_code, permissions, grant_results):
                    if grant_results and grant_results[0] == PackageManager.PERMISSION_GRANTED:
                        initiate_phone_call(phone_number=phone_number)
                    else:
                        logging.error("Phone call Permissions Denied")

                onRequestPermissionResult = permission_callback

