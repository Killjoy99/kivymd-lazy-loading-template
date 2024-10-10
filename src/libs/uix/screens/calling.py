import logging

from kivy.properties import StringProperty
from kivy.utils import platform
from kivymd.uix.screen import MDScreen

# Logger to capture events and errors
logger = logging.getLogger(__name__)


class CallingScreen(MDScreen):
    """
    A screen for managing phone calls on Android. It handles permission requests
    and phone call initiation, specifically designed for the Android platform.
    """

    phone_number = StringProperty("0776471033")  # Default phone number

    def on_enter(self):
        """Called when the screen is entered. Requests necessary permissions on Android."""
        if platform == "android":
            logger.info("Requesting Android permissions.")
            self.request_android_permissions()

    def request_android_permissions(self):
        """
        Requests necessary Android permissions required to make a phone call.
        These permissions include external storage, camera, and call permissions.
        """
        try:
            from android.permissions import Permission, request_permissions

            # Callback function to handle the results of the permission request
            def callback(permissions, results):
                for permission, result in zip(permissions, results):
                    if result:
                        logger.info(f"Permission granted: {permission}")
                    else:
                        logger.warning(f"Permission denied: {permission}")
                        # Optionally, notify the user that certain features won't work

            # Request permissions necessary for phone calls
            request_permissions(
                [
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.CAMERA,
                    Permission.CALL_PHONE,  # Permission to make phone calls
                ],
                callback,
            )
        except ImportError as e:
            logger.error(f"Android permissions module not found: {e}")
        except Exception as e:
            logger.error(f"Error while requesting permissions: {e}")

    def make_phone_call(self, phone_number: str):
        """
        Initiates a phone call to the given number, assuming permissions have been granted.

        :param phone_number: The phone number to call.
        """
        if not phone_number or not self.validate_phone_number(phone_number):
            logger.warning(f"Invalid phone number provided: {phone_number}")
            # Optionally, show a message to the user about invalid number
            return

        try:
            from android.permissions import Permission, check_permission
            from jnius import autoclass

            # Check if CALL_PHONE permission is granted
            if not check_permission(Permission.CALL_PHONE):
                logger.warning("CALL_PHONE permission not granted")
                # Optionally, notify the user about the missing permission (e.g., through a dialog)
                return

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

    def validate_phone_number(self, phone_number: str) -> bool:
        """
        Validates the phone number format to ensure it is valid before making a call.

        :param phone_number: The phone number to validate.
        :return: True if the phone number is valid, False otherwise.
        """
        # Basic check for valid phone number (this can be enhanced with regex)
        if phone_number and phone_number.isdigit() and len(phone_number) >= 10:
            return True
        return False
