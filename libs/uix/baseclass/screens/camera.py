import logging
import os
from datetime import datetime

from jnius import autoclass
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

from libs.applibs.utils import abs_path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class CameraScreen(MDScreen):
    # Property to hold the shared Username
    username = StringProperty()

    def on_enter(self):
        try:
            # Set the username as the username in the shared data storage
            self.username = self.manager.get_shared_data("username")
            if self.manager:
                # Bind the shared_data to the update_username method
                self.manager.bind(shared_data=self.update_username)

            # Play the camera
            self.ids.camera.play = True
            logging.info("Camera started.")
        except Exception as e:
            logging.error(f"Error on entering screen: {e}")

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

    def take_picture(self):
        try:
            # Get the camera widget
            camera = self.ids.camera

            # Define the file path to save the photo
            file_date = datetime.now()
            file_name = f"{file_date.year}{file_date.month}{file_date.day}_{file_date.hour}{file_date.minute}{file_date.second}"
            image_path = abs_path(f"data/captures/{file_name}.jpg")

            # Ensure the directory exists
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            # Capture the current frame from the camera feed
            camera.export_to_png(image_path)
            logging.info(f"Picture taken and saved to: {image_path}")

            # Update the label with the file path
            self.ids.label.text = f"Image saved to: {image_path}"

            # Make a toast with pyjnius for the save location
            Toast = autoclass("android.widget.Toast")
            Context = autoclass("android.content.Context")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            context = PythonActivity.mActivity.getApplicationContext()
            # Display the toast message
            toast = Toast.makeText(context, "Image Captured", Toast.LENGTH_SHORT)
            toast.show()

        except Exception as e:
            logging.error(f"Error taking picture: {e}")
            self.ids.label.text = "Failed to take picture."
