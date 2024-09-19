import io
import logging
from datetime import datetime

from jnius import autoclass
from kivy import platform
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from PIL import Image

from libs.applibs.utils import abs_path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CameraScreen(MDScreen):
    # Property to hold the shared Username
    username = StringProperty()
    camera_id = 0  # Default camera ID

    def on_pre_enter(self):
        if platform == "android":
            # Try to request permission when we enter this screen
            from android.permissions import Permission, request_permissions

            request_permissions(
                [
                    Permission.CAMERA,
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.RECORD_AUDIO,
                ]
            )

    def on_enter(self):
        try:
            # Set the username as the username in the shared data storage
            self.username = self.manager.get_shared_data("username")
            if self.manager:
                # Bind the shared_data to the update_username method
                self.manager.bind(shared_data=self.update_username)
            # Play the camera
            Clock.schedule_once(self.start_camera)

        except Exception as e:
            logging.error(f"Error on entering screen: {e}")

    def start_camera(self, dt):
        self.ids.camera.play = True
        logging.info("Camera started.")

    def on_leave(self):
        try:
            # Stop the camera on exit
            self.ids.camera.play = False
            logging.info("Camera stopped.")
        except Exception as e:
            logging.error(f"Error on leaving screen: {e}")

    def update_username(self, instance, value):
        """Callback function to update the screen data when shared data changes."""
        self.username = value.get("username", "")
        logging.info(f"Username updated: {self.username}")

    def get_device_rotation(self):
        # Access the android rotation services
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Context = autoclass("android.content.Context")
        WindowManager = autoclass("android.view.WindowManager")
        Display = autoclass("android.view.Display")
        DisplayRotation = autoclass("android.view.Surface")

        context = PythonActivity.mActivity.getApplicationContext()
        wm = context.getSystemService(Context.WINDOW_SERVICE)
        display = wm.getDefaultDisplay()
        rotation = display.getRotation()

        # Map the rotation value to degrees
        rotation_degrees = {
            DisplayRotation.ROTATION_0: 0,
            DisplayRotation.ROTATION_90: 90,
            DisplayRotation.ROTATION_180: 180,
            DisplayRotation.ROTATION_270: 270,
        }.get(rotation, 0)

        return rotation_degrees

    def take_picture(self):
        try:
            # Get the camera widget
            camera = self.ids.camera

            # Define the file path to save the photo
            file_date = datetime.now()
            file_name = f"{file_date.year}{file_date.month}{file_date.day}_{file_date.hour}{file_date.minute}{file_date.second}"

            # if on android, save image to external storage
            if platform == "android":
                from android.storage import (  # noqa: F401
                    primary_external_storage_path,
                    secondary_external_storage_path,
                )

                primary_ext_storage = primary_external_storage_path()
                image_path = f"{primary_ext_storage}/{file_name}.jpg"
            else:
                image_path = abs_path(f"data/captures/{file_name}.jpg")

            # Capture the current frame from the camera feed
            camera.export_to_png(image_path)

            # Open the captured image
            with open(image_path, "rb") as f:
                img = Image.open(io.BytesIO(f.read()))
                # Rotate the image if needed (e.g., by 90 degrees)
                img = img.rotate(90, expand=True)
                img.save(image_path)

            # Update the label with the file path
            self.ids.label.text = f"Image saved to: {image_path}"
            logging.info(f"Picture taken and saved to: {image_path}")

        except Exception as e:
            logging.error(f"Error taking picture: {e}")
            self.ids.label.text = "Failed to take picture."

    def switch_camera(self):
        try:
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Camera = autoclass("android.hardware.Camera")
            camera_info = autoclass("android.hardware.Camera$CameraInfo")

            num_cameras = Camera.getNumberOfCameras()
            if num_cameras <= 1:
                logging.info("Only one camera available.")
                return

            camera_info_list = [camera_info() for _ in range(num_cameras)]
            Camera.getCameraInfo(self.camera_id, camera_info_list[self.camera_id])

            # Switch to the next camera
            self.camera_id = (self.camera_id + 1) % num_cameras
            logging.info(f"Switched to camera {self.camera_id}")

            # Stop the current camera
            self.ids.camera.play = False

            # Set the new camera
            self.ids.camera.camera_id = self.camera_id
            self.ids.camera.play = True

        except Exception as e:
            logging.error(f"Error switching camera: {e}")
