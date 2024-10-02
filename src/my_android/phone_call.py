# my_android/phone_call.py
from jnius import autoclass
from my_android.permissions import (
    Intent,
    Uri,
    current_activity,
)

PythonActivity = autoclass("org.kivy.android.PythonActivity")


def initiate_phone_call(phone_number):
    intent = Intent(Intent.ACTION_CALL)
    uri = Uri.parse(f"tel:{phone_number}")
    intent.setData(uri)

    current_activity.startActivity(intent)
