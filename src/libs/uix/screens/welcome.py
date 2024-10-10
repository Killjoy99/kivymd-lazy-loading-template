import logging

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

# Setting up logger for the WelcomeScreen
logger = logging.getLogger(__name__)


class WelcomeScreen(MDScreen):
    """
    WelcomeScreen handles the first interaction with the user. It manages
    preloading the next screens, updating user information, and cache management.
    """

    status = StringProperty("")  # Status message shown to the user

    def on_enter(self):
        """Called when entering the screen. Preloads potential next screens."""
        logger.info("Entering WelcomeScreen, preparing to preload next screens.")
        # Preload the next likely screen to reduce load time
        Clock.schedule_once(self.preload_next)

    def preload_next(self, dt) -> None:
        """
        Preloads the 'settings' screen for faster future navigation.
        This reduces transition delays.
        """
        self.manager.preload_screens(["settings"])  # Preload the settings screen
        self.status = "Screens preloaded successfully"
        logger.info(self.status)
        print(self.manager._screen_cache)

    def login(self, new_name: str) -> None:
        """
        Logs in the user by updating the shared username and transitioning to the home screen.

        :param new_name: The new username to be set.
        """
        if not new_name:
            logger.warning("Attempt to log in with an empty name.")
            self.status = "Name cannot be empty"
            return

        logger.info(f"Changing name to: {new_name}")
        self.manager.set_shared_data("username", new_name)  # Store the new username
        self.manager.push_replacement("home")  # Navigate to the home screen
        logger.info("User logged in, navigating to home screen.")

    def on_leave(self):
        """
        Called when leaving the screen. Removes this screen from cache to free up memory.
        """
        logger.info(f"Leaving {self.name}, removing screen from cache.")
        self.manager.remove_screen_from_cache(
            self.name
        )  # Remove this screen from cache
