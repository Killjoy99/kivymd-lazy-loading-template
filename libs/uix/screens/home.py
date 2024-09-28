import logging

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

logger = logging.getLogger(__name__)


class HomeScreen(MDScreen):
    username = StringProperty("Change Me")  # Kivy's StringProperty handles the type

    def on_enter(self):
        """Called when entering the screen. Preloads potential next screens."""
        # Preload the next likely screen (optional) to reduce load times and help in transitioning
        Clock.schedule_once(self.preload_next)
        # Update username from shared data store
        self.username = self.manager.get_shared_data("username")

    def preload_next(self, dt) -> None:
        """Preload settings"""
        self.manager.preload_screens(["settings"])
