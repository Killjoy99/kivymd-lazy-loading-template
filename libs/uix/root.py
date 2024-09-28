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


################################################# OPTIMISED DATA SHARING METHODS ####################################


class Root(MDScreenManager):
    history = deque()  # List of tuples (screen_name, side)
    shared_data = {}

    _screen_cache = {}  # Cache screens for faster loading
    _kv_cache = {}  # Cache KV so they dont get loaded every single time
    _preload_cache = {}  # Track preloaded screens
    back_press_count = 0  # Track back button presses
    back_press_timer = None  # Timer reference for resseting the back_press_count

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self._handle_keyboard)

        try:
            with open(file_utils.abs_path("assets/screens.json")) as f:
                self.screens_data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error loading screens data: {e}")
            self.screens_data = {}

    def push(
        self, screen_name: str, side: str = "left", transition_type: str = "slide"
    ) -> None:
        """Appends the screen to the navigation history and sets `screen_name` as the current screen."""
        if self.current != screen_name:
            self.history.append((screen_name, side))

        # profile the screen loading logic
        # self.profile = cProfile.Profile()
        # self.profile.enable()

        self.load_screen(screen_name)

        # self.profile.disable()
        # self.profile.dump_stats("tests/loading_screen.profile")

        if transition_type == "slide":
            self.transition.direction = side
        elif transition_type == "fade":
            self.transition = FadeTransition()
        else:
            logging.warning(
                f"Unknown transition type: {transition_type}. Defaulting to 'slide'."
            )
            self.transition.direction = side

        self.current = screen_name

    def push_replacement(
        self, screen_name: str, side: str = "left", transition_type: str = "slide"
    ) -> None:
        """Clears the navigation history and sets the current screen to `screen_name`."""
        self.history.clear()
        self.push(screen_name, side, transition_type)

    def preload_screens(self, screen_names: list) -> None:
        """Preloads the specified screens in the background for faster navigation."""
        for screen_name in screen_names:
            if (
                screen_name not in self._screen_cache
                and screen_name not in self._preload_cache
            ):
                self.load_screen(screen_name, preload=True)

    def clear_cache(self) -> None:
        """Clears the screen and KV caches to free up memory."""
        self._screen_cache.clear()
        self._kv_cache.clear()
        logging.info("Caches cleared.")

    def remove_widget_only(self, screen_name: str) -> None:
        """
        Removes the screen widget from the ScreenManager but keeps the screen in the cache.
        This is useful for freeing widget resources while keeping the cached screen object.
        """
        if screen_name in self._screen_cache:
            screen = self._screen_cache[screen_name]
            if self.has_screen(screen_name):
                self.remove_widget(screen)
                logging.info(
                    f"Screen widget {screen_name} removed from the ScreenManager but kept in cache."
                )
            else:
                logging.warning(
                    f"Screen {screen_name} is not currently loaded in the ScreenManager."
                )

    def remove_screen_from_cache(self, screen_name: str) -> None:
        """
        Removes a screen from both the cache and the ScreenManager, freeing up memory completely.
        """
        if screen_name in self._screen_cache:
            screen = self._screen_cache.pop(screen_name)
            if self.has_screen(screen_name):
                self.remove_widget(screen)
            logging.info(
                f"Screen {screen_name} removed from both cache and ScreenManager."
            )
        else:
            logging.warning(f"Screen {screen_name} not found in cache.")

    def back(self) -> None:
        """Removes the current screen from the navigation history and sets the current screen to the previous one."""
        if len(self.history) <= 1:
            self.back_press_count += 1
            if self.back_press_count == 2:
                MDApp.get_running_app().stop()  # Exit the app
            else:
                logging.info("Press back again to exit.")

                # Reset back_press_count after 2 seconds
                if self.back_press_timer:
                    self.back_press_timer.cancel()  # Cancel any existing timer
                self.back_press_timer = Clock.schedule_once(
                    self.reset_back_press_count, 2
                )
            return
        else:
            self.back_press_count = 0  # Reset counter if navigating back

        _cur_screen, cur_side = self.history.pop()
        prev_screen, _ = self.history[-1]

        self.transition.direction = {
            "left": "right",
            "right": "left",
            "up": "down",
            "down": "up",
        }.get(cur_side, "left")

        self.current = prev_screen

    def reset_back_press_count(self, dt: float) -> None:
        """Resets the back press count after the specified duration."""
        self.back_press_count = 0

    def set_shared_data(self, key: str, value: Optional[any]) -> None:
        """Sets a key-value pair in the shared data store."""
        self.shared_data[key] = value

    def get_shared_data(self, key: str) -> Optional[any]:
        """Returns the value associated with `key` in the shared data store."""
        return self.shared_data.get(key, None)

    def _handle_keyboard(self, instance, key: int, *args) -> bool:
        if key == 27:  # ESC key
            self.back()
            return True

    # profile the screen loading

    def load_screen(self, screen_name: str, preload: bool = False) -> None:
        """Creates an instance of the screen object and adds it to the screen manager."""
        if self.has_screen(screen_name):
            return  # Screen already loaded

        if screen_name in self._screen_cache:
            screen_object = self._screen_cache[screen_name]
        else:
            screen = self.screens_data.get(screen_name)
            if not screen:
                logging.warning(f"Screen {screen_name} not found in screens data.")
                return

            try:
                # Load KV file
                kv_path = screen.get("kv")
                if kv_path and kv_path not in self._kv_cache:
                    kv_file_path = file_utils.abs_path(kv_path)
                    try:
                        Builder.load_file(kv_file_path)
                        self._kv_cache[kv_path] = True
                    except FileNotFoundError:
                        logging.error(f"KV file {kv_file_path} not found.")

                # Import screen class dynamically
                module_name = screen.get("module")
                class_name = screen.get("class")

                if not module_name or not class_name:
                    logging.warning(
                        f"Missing 'module' or 'class' in screen data for {screen_name}."
                    )
                    return

                try:
                    module = importlib.import_module(module_name)
                    screen_class = getattr(module, class_name)
                except (ImportError, AttributeError) as e:
                    logging.error(
                        f"Error importing class {class_name} from module {module_name}: {e}"
                    )
                    return

                screen_object = screen_class()
                screen_object.name = screen_name

                if preload:
                    self._preload_cache[screen_name] = screen_object
                    logging.info(f"Screen {screen_name} preloaded.")
                else:
                    self._screen_cache[screen_name] = screen_object
                    self.add_widget(screen_object)

            except FileNotFoundError:
                logging.error(f"Screen {screen_name} definition file not found.")
            except Exception as e:
                logging.error(f"Unexpected error loading screen {screen_name}: {e}")
