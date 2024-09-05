from kivymd.uix.screen import MDScreen

from libs.applibs.utils import DataDispatcher


class AuthScreen(DataDispatcher, MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def login(self):
        user_data = {"username": "Philani"}

        self.share_data(user_data)
        # change to home screen
        self.manager.push_replacement("home")
