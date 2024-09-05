import asyncio

from kivymd.uix.screen import MDScreen

from libs.applibs.connection_manager import ConnectionManager, client


class WelcomeScreen(MDScreen):
    def login(self):
        username = "Philani"
        self.manager.set_shared_data("username", username)
        # change to home screen
        self.manager.push_replacement("home", transition_type="fade")

    def on_enter(self):
        self.test_google()

    def test_google(self):
        asyncio.create_task(self.async_test_google())

    async def async_test_google(self):
        connect = ConnectionManager(client=client)
        await connect.get_google()
