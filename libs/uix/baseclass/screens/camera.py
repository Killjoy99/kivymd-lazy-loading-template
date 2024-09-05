from datetime import datetime

from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

from libs.applibs.utils import abs_path


class CameraScreen(MDScreen):
    # Property to hold the shared Username
    username = StringProperty()

    def on_enter(self):
        # set the username as the usernae in the shared data storage
        self.username = self.manager.get_shared_data("username")
        if self.manager:
            # Bind the shared_data to the update_example_data method
            self.manager.bind(shared_data=self.update_username)

        # Play the camera
        self.ids.camera.play = True

    def on_leave(self):
        # stop the camera on exit
        self.ids.camera.play = False

    def update_username(self, instance, value):
        """Callback function to update the screen data when shared data changes."""
        self.username = value.get("username", "")

    def take_picture(self):
        # get the camera widget
        camera = self.ids.camera

        # define the file path to save the photo
        file_date = datetime.now()
        file_name = f"{file_date.year}{file_date.month}{file_date.day}_{file_date.hour}{file_date.minute}{file_date.second}"
        image_path = abs_path(f"data/captures/{file_name}.jpg")

        # Capture the current frame from the camera feed
        camera.export_to_png(image_path)

        # Update the label with the filePath
        self.ids.label.text = f"Image saved to: {image_path}"
