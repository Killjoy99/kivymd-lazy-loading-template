from httpx import ConnectError
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from libs.applibs.connection_manager import client, get_google


class NetworkScreen(MDScreen):
    response_text = ObjectProperty("")

    def on_enter(self):
        # try to connect to google
        try:
            response = get_google(client)
            if not response:
                self.response_text = "Cannot Reach Google servers"
            else:
                self.response_text = "Connected to google"

        except ConnectError:
            self.response_text = "Cannot Reach Google servers"
