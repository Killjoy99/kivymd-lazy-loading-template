import importlib
import json
import logging
from typing import Optional

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import DictProperty
from kivy.uix.screenmanager import FadeTransition
from kivymd.uix.screenmanager import MDScreenManager

from libs.applibs import utils

logging.basicConfig(level=logging.INFO)
################################################# OPTIMISED DATA SHARING METHODS ####################################


class Root(MDScreenManager):
    history = []  # List of tuples (screen_name, side)
    shared_data = DictProperty()
    # Cache screens for faster loading
    _screen_cache = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shared_data = {}
        Window.bind(on_keyboard=self._handle_keyboard)

        try:
            with open(utils.abs_path("screens.json")) as f:
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

        self.load_screen(screen_name)

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

    def back(self) -> None:
        """Removes the current screen from the navigation history and sets the current screen to the previous one."""
        if len(self.history) <= 1:
            logging.info("No previous screen to back to.")
            return

        cur_screen, cur_side = self.history.pop()
        prev_screen, _ = self.history[-1]

        self.transition.direction = {
            "left": "right",
            "right": "left",
            "up": "down",
            "down": "up",
        }.get(cur_side, "left")

        self.current = prev_screen

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

    def load_screen(self, screen_name: str) -> None:
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
                if kv_path:
                    kv_file_path = utils.abs_path(kv_path)
                    try:
                        Builder.load_file(kv_file_path)
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
                self._screen_cache[screen_name] = screen_object
                self.add_widget(screen_object)

            except FileNotFoundError:
                logging.error(f"Screen {screen_name} definition file not found.")
            except Exception as e:
                logging.error(f"Unexpected error loading screen {screen_name}: {e}")
