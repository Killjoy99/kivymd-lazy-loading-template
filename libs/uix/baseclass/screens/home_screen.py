from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen


class HomeScreen(MDScreen):
    # Property to hold the shared Username
    username = StringProperty()

    def on_enter(self):
        # set the username as the usernae in the shared data storage
        self.username = self.manager.get_shared_data("username")
        if self.manager:
            # Bind the shared_data to the update_example_data method
            self.manager.bind(shared_data=self.update_username)

    def update_username(self, instance, value):
        """Callback function to update the screen data when shared data changes."""
        self.username = value.get("username", "")
