import logging

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

logger = logging.getLogger(__name__)


class WelcomeScreen(MDScreen):
    username = StringProperty("Change Me")  # Kivy's StringProperty handles the type
    status = StringProperty("")

    def on_enter(self):
        """Called when entering the screen. Preloads potential next screens."""
        # Preload the next likely screen (optional) to reduce load times and help in transitioning
        Clock.schedule_once(self.preload_next)

    def preload_next(self, dt) -> None:
        """Preload the next screens for faster navigation.

        Args:
            dt (float): Time delay (passed by Clock). Not used directly.
        """
        self.manager.preload_screens(
            ["hello_screen", "settings_screen", "profile_screen"]
        )
        self.status = "Screens preloaded successfully"

    def change_name(self, new_name: str) -> None:
        """Change the user's name and store it in shared data."""
        logger.info(f"Changing name to: {new_name}")
        self.username = new_name  # This updates the UI dynamically
        self.manager.set_shared_data("username", new_name)

    def on_leave(self):
        """Called when leaving the screen. Removes this screen from cache."""
        # Remove this screen from the cache as it will never be needed anymore
        self.manager.remove_screen_from_cache(self.name)
