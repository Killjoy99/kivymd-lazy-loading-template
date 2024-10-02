from my_android.permissions import request_phone_permission, PythonActivity, Intent, Uri
import logging

# Method to make a phone call
def initiate_phone_call(phone_number: str):
    current_activity = PythonActivity.mActivity
    intent = Intent(Intent.ACTION_CALL)
    intent.setData(Uri.parse(f"tel:{phone_number}"))
    current_activity.startActivity(intent)