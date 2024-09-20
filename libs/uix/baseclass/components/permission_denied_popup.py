from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import (  # noqa: F401
    MDDialog,
    MDDialogButtonContainer,
    MDDialogContentContainer,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivymd.uix.label import MDLabel


def show_permission_denied_popup():
    layout = MDBoxLayout(orientation="vertical", padding=10)

    label = MDLabel(
        text="Permissions denied. Camera cannot be used without the necessary permissions."
    )
    dismiss_button = Button(text="Dismiss", size_hint=(1, 0.25))

    layout.add_widget(label)
    layout.add_widget(dismiss_button)

    popup = Popup(title="Permissions Denied", content=layout, size_hint=(0.8, 0.4))
    # popup = MDDialog(
    #     MDDialogHeadlineText(text="Permissions Denied"),
    #     MDDialogButtonContainer(
    #         MDButton(
    #             MDButtonText(
    #                 text="Dismiss", pos_hint={"center_x": 0.5, "center_y": 0.5}
    #             )
    #         )
    #     ),
    # )

    dismiss_button.bind(on_press=popup.dismiss)
    popup.open()
