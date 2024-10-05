import logging

from kivy.properties import StringProperty
from kivy.utils import platform
from kivymd.uix.screen import MDScreen

logger = logging.getLogger(__name__)


class CallingScreen(MDScreen):
    phone_number = StringProperty("0776471033")  # Default phone number

    def on_enter(self):
        if platform == "android":
            self.request_android_permissions()

    def request_android_permissions(self):
        try:
            from android.permissions import Permission, request_permissions

            def callback(permissions, results):
                for permission, result in zip(permissions, results):
                    if result:
                        logger.info(f"Permission granted: {permission}")
                    else:
                        logger.warning(f"Permission denied: {permission}")

            request_permissions(
                [
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.CAMERA,
                    Permission.CALL_PHONE,  # Permission to make phone calls
                ],
                callback,
            )
        except Exception as e:
            logger.error(f"Error while requesting permissions: {e}")

    def make_phone_call(self, phone_number: str):
        try:
            from jnius import autoclass

            # Get the Android Intent and Uri classes
            Intent = autoclass("android.content.Intent")
            Uri = autoclass("android.net.Uri")

            # Create an intent to initiate a call
            intent = Intent(Intent.ACTION_CALL)
            uri = Uri.parse(f"tel:{phone_number}")
            intent.setData(uri)

            # Get the current Android activity and start the call intent
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity
            activity.startActivity(intent)

            logger.info(f"Initiating call to {phone_number}")

        except Exception as e:
            logger.error(f"Error while making the phone call: {e}")
