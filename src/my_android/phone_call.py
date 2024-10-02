from jnius import autoclass, cast
from my_android.permissions import request_phone_permission, PythonActivity, Intent, Uri


# Method to make a phone call
def make_phone_call(phone_number: str):
    if request_phone_permission():
        current_activity = PythonActivity.mActivity
        intent = Intent(Intent.ACTION_CALL)
        intent.setData(Uri.parse(f"tel:{phone_number}"))
        current_activity.startActivity(intent)
    else:
        print("Phone call permission not granted")