from kivymd.uix.screen import MDScreen

from libs.applibs.utils import DataDispatcher


class HomeScreen(DataDispatcher, MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_data_shared=self.receive_data)

    def receive_data(self, instance, data):
        print(f"Received data:: {data}")
