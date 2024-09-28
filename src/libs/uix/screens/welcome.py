import logging

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

logger = logging.getLogger(__name__)


class WelcomeScreen(MDScreen):
    status = StringProperty("")

    def on_enter(self):
        """Called when entering the screen. Preloads potential next screens."""
        # Preload the next likely screen (optional) to reduce load times and help in transitioning
        Clock.schedule_once(self.preload_next)

    def preload_next(self, dt) -> None:
        """Preload the home Screen"""
        self.manager.preload_screens(["settings"])
        self.status = "Screens preloaded successfully"

    def login(self, new_name: str) -> None:
        """Change the user's name and store it in shared data."""
        logger.info(f"Changing name to: {new_name}")
        self.manager.set_shared_data("username", new_name)
        self.manager.push_replacement("home")

    def on_leave(self):
        """Called when leaving the screen. Removes this screen from cache."""
        # Remove this screen from the cache as it will never be needed anymore
        self.manager.remove_screen_from_cache(self.name)
