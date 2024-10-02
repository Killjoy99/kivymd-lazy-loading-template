import pytest
from kivy.base import EventLoop
from kivymd.app import MDApp

from ..src.libs.uix.root import Root


@pytest.fixture(scope="module", autouse=True)
def app():
    # Start the Kivy Event Loop
    EventLoop.ensure_window()
    app = MDApp()
    app.root = Root()
    app.run()
    yield app
    app.stop()


def test_welcome_screen_exists(app):
    welcome_screen = app.root.get_screen("welcome")
    assert welcome_screen is not None, "Welcome screen should exist"


def test_welcome_screen_status_initialization(app):
    welcome_screen = app.root.get_screen("welcome")
    assert welcome_screen.status == "", "Initial status should be empty"
