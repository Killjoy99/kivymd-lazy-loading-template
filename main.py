import logging
from jnius import autoclass
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

if platform != "android":
    Window.size = (420, 840)

from libs.uix.root import Root


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
        self.permission_dialog = None

    def build(self):
        # Initialize the root widget
        self.root = Root()
        self.root.push("welcome")

        # Request for permission if running on Android
        if platform == "android":
            self.show_permission_dialog()

    def show_permission_dialog(self):
        if not self.permission_dialog:
            self.permission_dialog = MDDialog(
                title="Permissions Required",
                text="This app requires certain permissions to function properly. Please grant the required permissions.",
                buttons=[
                    MDRaisedButton(
                        text="Grant Permissions",
                        on_release=self.request_android_permissions
                    ),
                    MDRaisedButton(
                        text="Cancel",
                        on_release=self.dismiss_permission_dialog
                    )
                ]
            )
        self.permission_dialog.open()

    def dismiss_permission_dialog(self, *args):
        if self.permission_dialog:
            self.permission_dialog.dismiss()

    def request_android_permissions(self, *args):
        try:
            # Access the Android activity
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Activity = autoclass("android.app.Activity")
            ContextCompat = autoclass("androidx.core.app.ContextCompat")
            ActivityCompat = autoclass("androidx.core.app.ActivityCompat")
            Toast = autoclass("android.widget.Toast")

            # Get the activity
            activity = PythonActivity.mActivity

            # List Permissions to request
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

            # Request for each permission
            for permission in permissions:
                if (
                    ContextCompat.checkSelfPermission(activity, permission)
                    != Activity.PERMISSION_GRANTED
                ):
                    ActivityCompat.requestPermissions(activity, [permission], 0)
                    logging.info(f"Requested permission: {permission}")

            # Show a toast message to inform the user
            self.show_toast("Permissions request sent.")

            # Dismiss the dialog after requesting permissions
            self.dismiss_permission_dialog()

        except Exception as e:
            logging.error(f"Error requesting permissions: {e}")

    def show_toast(self, message):
        Toast = autoclass("android.widget.Toast")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        activity = PythonActivity.mActivity
        Toast.makeText(activity, message, Toast.LENGTH_SHORT).show()

    def on_request_permissions_result(self, request_code, permissions, grant_results):
        Toast = autoclass("android.widget.Toast")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        activity = PythonActivity.mActivity

        for permission, grant_result in zip(permissions, grant_results):
            if grant_result == autoclass("android.content.pm.PackageManager").PERMISSION_GRANTED:
                self.show_toast(f"Permission granted: {permission}")
            else:
                self.show_toast(f"Permission denied: {permission}")

    def check_permissions(self, *args, **kwargs):
        if platform == "android":
            try:
                # Access the Android Activity
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                ActivityCompat = autoclass("androidx.core.app.ActivityCompat")
                Activity = autoclass("android.app.Activity")

                # Get the activity
                activity = PythonActivity.mActivity

                # List Permissions to check
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

                # Check for each permission
                all_granted = True
                for permission in permissions:
                    if (
                        ActivityCompat.checkSelfPermission(activity, permission)
                        != Activity.PERMISSION_GRANTED
                    ):
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
        # Show a message or dialog to the user
        logging.warning(message)
        self.show_toast(message)
        # Guide the user to enable it in the settings
        # Alternatively restrict access to the resource that needs the permissions


if __name__ == "__main__":
    MainApp().run()
