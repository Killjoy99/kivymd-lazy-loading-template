import os

from kivy.event import EventDispatcher

from libs.applibs import constants


def abs_path(*path):
    return os.path.join(constants.PROJECT_DIR, *path)


class DataDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        super(DataDispatcher, self).__init__(**kwargs)
        self.register_event_type("on_data_shared")

    def share_data(self, data):
        self.dispatch("on_data_shared", data)

    def on_data_shared(self, data):
        pass
