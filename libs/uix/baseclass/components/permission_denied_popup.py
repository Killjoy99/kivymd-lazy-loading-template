from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


def show_permission_denied_popup():
    layout = BoxLayout(orientation="vertical", padding=10)

    label = Label(
        text="Permissions denied. Camera cannot be used without the necessary permissions."
    )
    dismiss_button = Button(text="Dismiss", size_hint=(1, 0.25))

    layout.add_widget(label)
    layout.add_widget(dismiss_button)

    popup = Popup(title="Permission Denied", content=layout, size_hint=(0.8, 0.4))

    dismiss_button.bind(on_press=popup.dismiss)
    popup.open()
