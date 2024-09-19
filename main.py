import cProfile  # noqa: F401
import logging

from jnius import autoclass
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

        if platform == "android":
            # Deactivate the loading screen
            from android import loading_screen

            loading_screen.hide_loading_screen()

            # Request permissions if running on Android
            self.request_android_permissions()
        else:
            Window.size = (420, 840)

        # Initialize the root widget
        self.root = Root()
        self.root.push("welcome")

    def request_android_permissions(self):
        from android.permissions import Permission, request_permissions

        try:
            request_permissions([Permission.INTERNET])
        except Exception as e:
            logging.error(f"Failed to get permissions: {e}")

    def check_permissions(self):
        if platform == "android":
            try:
                # Access the Android Activity
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                ActivityCompat = autoclass("androidx.core.app.ActivityCompat")

                # Get the activity
                activity = PythonActivity.mActivity

                # Permissions to check
                permissions = [
                    "android.permission.CAMERA",
                    "android.permission.INTERNET",
                    "android.permission.WRITE_EXTERNAL_STORAGE",
                    "android.permission.ACCESS_FINE_LOCATION",
                    "android.permission.ACCESS_COARSE_LOCATION",
                    "android.permission.READ_EXTERNAL_STORAGE",
                    "android.permission.RECORD_AUDIO",
                    "android.permission.VIBRATE",
                    "android.permission.WAKE_LOCK",
                ]

                # Check permissions
                all_granted = True
                for permission in permissions:
                    if ActivityCompat.checkSelfPermission(activity, permission) != 0:
                        all_granted = False
                        logging.fatal(f"Permission not granted for {permission}")
                        break

                if all_granted:
                    logging.info("All permissions granted")

            except Exception as e:
                logging.error(f"Error checking permissions: {e}")

    def handle_permission_denied(self, permission):
        # Inform the user about the denied permission
        permission_messages = {
            "android.permission.CAMERA": "Camera permission required for taking pictures.",
            "android.permission.WRITE_EXTERNAL_STORAGE": "Storage permission required for saving data.",
        }

        message = permission_messages.get(permission, "Permission denied.")
        logging.warning(message)
        # Guide the user to enable it in the settings
        # Alternatively, restrict access to the resource that needs the permissions


if __name__ == "__main__":
    MainApp().run()
