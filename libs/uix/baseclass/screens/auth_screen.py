from kivymd.uix.screen import MDScreen


class AuthScreen(MDScreen):
    def login(self):
        username = "Philani"
        self.manager.set_shared_data("username", username)
        # change to home screen
        self.manager.push_replacement("home", transition_type="fade")
