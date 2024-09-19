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
        if platform != "android":
            Window.size = (420, 840)

        # Request permissions if running on Android
        if platform == "android":
            self.request_android_permissions()

        # Initialize the root widget
        self.root = Root()
        self.root.push("welcome")

    def request_android_permissions(self):
        if platform == "android":
            try:
                # Access the Android activity
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                ActivityCompat = autoclass("androidx.core.app.ActivityCompat")
                ContextCompat = autoclass("androidx.core.app.ContextCompat")

                # Get the activity
                activity = PythonActivity.mActivity

                # Permissions to request
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

                # Request permissions
                for permission in permissions:
                    if ContextCompat.checkSelfPermission(activity, permission) != 0:
                        ActivityCompat.requestPermissions(activity, [permission], 0)
                        logging.info(f"Requested permission: {permission}")

            except Exception as e:
                logging.error(f"Error requesting permissions: {e}")

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

    # def on_start(self):
    #     self.profile = cProfile.Profile()
    #     self.profile.enable()

    # def on_stop(self):
    def on_stop(self):
        """Called when the app is stopping."""
        self.executor.shutdown(wait=True)  # Wait for all tasks to complete
        super().on_stop()

    #     self.profile.disable()
    #     self.profile.dump_stats("tests/myapp.profile")


if __name__ == "__main__":
    MainApp().run()
