from kivymd.uix.screen import MDScreen


class WelcomeScreen(MDScreen):
    def login(self):
        username = "Philani"
        self.manager.set_shared_data("username", username)
        # change to home screen
        self.manager.push("camera", transition_type="fade")
