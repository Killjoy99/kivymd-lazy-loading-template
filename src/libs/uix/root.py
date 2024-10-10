import importlib
import json
import logging
from collections import deque
from typing import Optional

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import FadeTransition
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from libs.applibs.utils import file_utils

logging.basicConfig(level=logging.INFO)


class Root(MDScreenManager):
    """
    The Root class manages screen transitions and caching for a Kivy-based application.
    It handles screen navigation, shared data, and memory management of screens using caches.
    """

    history = (
        deque()
    )  # List of tuples (screen_name, side) to track screen navigation history.
    shared_data = {}  # Global shared data store for inter-screen communication.

    # Caches to improve performance
    _screen_cache = {}  # Cache loaded screens to avoid reloading them.
    _kv_cache = {}  # Cache KV files to avoid re-loading them.
    _preload_cache = {}  # Cache for preloaded screens to speed up future loads.

    back_press_count = 0  # Tracks back button presses for exiting the app.
    back_press_timer = None  # Timer reference for resetting back_press_count.

    def __init__(self, **kwargs):
        """
        Initializes the Root screen manager, binds the back button handler,
        and loads screen data from the JSON configuration file.
        """
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self._handle_keyboard)

        # Load screen data from JSON configuration file.
        try:
            with open(file_utils.abs_path("assets/screens.json")) as f:
                self.screens_data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error loading screens data: {e}")
            self.screens_data = {}

    def push(
        self, screen_name: str, side: str = "left", transition_type: str = "slide"
    ) -> None:
        """
        Pushes a new screen onto the navigation stack and transitions to it.

        :param screen_name: Name of the screen to navigate to.
        :param side: The direction of the transition ('left', 'right', etc.).
        :param transition_type: The type of transition ('slide', 'fade', etc.).
        """
        if self.current != screen_name:
            self.history.append((screen_name, side))

        # Handle screen transition based on the type.
        self.set_transition(transition_type, side)
        self.load_screen(screen_name)
        self.current = screen_name

    def set_transition(self, transition_type: str, side: str) -> None:
        """
        Sets the transition type and direction for screen navigation.

        :param transition_type: The type of transition (slide, fade, etc.).
        :param side: The direction of the transition.
        """
        if transition_type == "slide":
            self.transition.direction = side
        elif transition_type == "fade":
            self.transition = FadeTransition()
        else:
            logging.warning(
                f"Unknown transition type: {transition_type}, defaulting to 'slide'."
            )
            self.transition.direction = side

    def push_replacement(
        self, screen_name: str, side: str = "left", transition_type: str = "slide"
    ) -> None:
        """
        Replaces the entire navigation stack with the new screen.

        :param screen_name: Name of the screen to set as the new root screen.
        :param side: Direction of the transition.
        :param transition_type: Type of transition.
        """
        self.history.clear()
        self.push(screen_name, side, transition_type)

    def preload_screens(self, screen_names: list) -> None:
        """
        Preloads a list of screens asynchronously to improve future load times.

        :param screen_names: List of screen names to preload.
        """
        for screen_name in screen_names:
            if (
                screen_name not in self._screen_cache
                and screen_name not in self._preload_cache
            ):
                Clock.schedule_once(
                    lambda dt: self.load_screen(screen_name, preload=True)
                )

    def clear_cache(self) -> None:
        """
        Clears the screen and KV caches to free up memory.
        """
        self._screen_cache.clear()
        self._kv_cache.clear()
        logging.info("Caches cleared.")

    def remove_widget_only(self, screen_name: str) -> None:
        """
        Removes a screen widget from the ScreenManager but keeps it in the screen cache.
        Useful for freeing up resources while maintaining a cached version of the screen.

        :param screen_name: Name of the screen to remove.
        """
        if screen_name in self._screen_cache:
            screen = self._screen_cache[screen_name]
            if self.has_screen(screen_name):
                self.remove_widget(screen)
                logging.info(f"Screen widget {screen_name} removed but kept in cache.")
            else:
                logging.warning(f"Screen {screen_name} is not currently loaded.")

    def remove_screen_from_cache(self, screen_name: str) -> None:
        """
        Completely removes a screen from both the cache and the ScreenManager.
        Frees up memory by fully unloading the screen.

        :param screen_name: Name of the screen to remove from the cache and ScreenManager.
        """
        if screen_name in self._screen_cache:
            screen = self._screen_cache.pop(screen_name)
            if self.has_screen(screen_name):
                self.remove_widget(screen)
            logging.info(f"Screen {screen_name} removed from cache and ScreenManager.")
        else:
            logging.warning(f"Screen {screen_name} not found in cache.")

    def back(self) -> None:
        """
        Handles the back navigation. If the history stack is empty, it prompts the user to
        press back twice to exit the app. Otherwise, navigates to the previous screen.
        """
        if len(self.history) <= 1:
            self._handle_back_press_to_exit()
            return

        self.back_press_count = 0  # Reset counter if navigating back.

        # Pop the current screen and navigate to the previous one.
        _cur_screen, cur_side = self.history.pop()
        prev_screen, _ = self.history[-1]
        self.transition.direction = self._reverse_direction(cur_side)
        self.current = prev_screen

    def _handle_back_press_to_exit(self) -> None:
        """
        Manages the logic to exit the app if back is pressed twice within 2 seconds.
        """
        self.back_press_count += 1
        if self.back_press_count == 2:
            MDApp.get_running_app().stop()  # Exit the app
        else:
            logging.info("Press back again to exit.")
            if not self.back_press_timer:
                self.back_press_timer = Clock.schedule_once(
                    self.reset_back_press_count, 2
                )

    def _reverse_direction(self, cur_side: str) -> str:
        """
        Returns the reverse direction of a given transition direction.

        :param cur_side: The current direction of transition.
        :return: The reversed transition direction.
        """
        return {"left": "right", "right": "left", "up": "down", "down": "up"}.get(
            cur_side, "left"
        )

    def reset_back_press_count(self, dt: float) -> None:
        """
        Resets the back press count after a delay, allowing the user to exit the app by pressing back twice.

        :param dt: The time duration after which the count is reset.
        """
        self.back_press_count = 0
        self.back_press_timer = None

    def set_shared_data(self, key: str, value: Optional[any]) -> None:
        """
        Sets a key-value pair in the shared data store.

        :param key: The key for the shared data.
        :param value: The value to be associated with the key.
        """
        self.shared_data[key] = value

    def get_shared_data(self, key: str) -> Optional[any]:
        """
        Retrieves a value from the shared data store by its key.

        :param key: The key for the shared data.
        :return: The value associated with the key, or None if not found.
        """
        return self.shared_data.get(key)

    def _handle_keyboard(self, instance, key: int, *args) -> bool:
        """
        Handles keyboard events, specifically the back button (ESC key).

        :param instance: The instance of the keyboard event.
        :param key: The key code of the pressed key.
        :return: True if the key event was handled, False otherwise.
        """
        if key == 27:  # ESC key
            self.back()
            return True

    def load_screen(self, screen_name: str, preload: bool = False) -> None:
        """
        Loads a screen dynamically by its name, either as a preloaded screen or for immediate display.

        :param screen_name: The name of the screen to load.
        :param preload: If True, the screen is preloaded into the cache without being displayed.
        """
        if self.has_screen(screen_name) or screen_name in self._screen_cache:
            return

        screen = self.screens_data.get(screen_name)
        if not screen:
            logging.warning(f"Screen {screen_name} not found in data.")
            return

        # Load KV file if not already cached
        kv_path = screen.get("kv")
        if kv_path and kv_path not in self._kv_cache:
            self._load_kv(kv_path)

        # Instantiate and cache the screen object
        screen_object = self._instantiate_screen(screen, screen_name)
        if not screen_object:
            return

        if preload:
            self._preload_cache[screen_name] = screen_object
        else:
            self._screen_cache[screen_name] = screen_object
            self.add_widget(screen_object)

    def _load_kv(self, kv_path: str) -> None:
        """
        Loads the KV file for the specified screen and caches it.

        :param kv_path: The path to the KV file.
        """
        kv_file_path = file_utils.abs_path(kv_path)
        try:
            Builder.load_file(kv_file_path)
            self._kv_cache[kv_path] = True
        except FileNotFoundError:
            logging.error(f"KV file {kv_file_path} not found.")

    def _instantiate_screen(self, screen: dict, screen_name: str):
        """
        Dynamically instantiates a screen class based on its module and class name.

        :param screen: A dictionary containing screen metadata (module and class).
        :param screen_name: The name of the screen to instantiate.
        :return: The instantiated screen object, or None if an error occurs.
        """
        module_name = screen.get("module")
        class_name = screen.get("class")

        if not module_name or not class_name:
            logging.warning(f"Missing 'module' or 'class' for screen {screen_name}.")
            return None

        try:
            module = importlib.import_module(module_name)
            screen_class = getattr(module, class_name)
            screen_object = screen_class()
            screen_object.name = screen_name
            return screen_object
        except (ImportError, AttributeError) as e:
            logging.error(f"Error loading {class_name} from {module_name}: {e}")
            return None
