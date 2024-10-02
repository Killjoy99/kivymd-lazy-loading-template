import logging

from jnius import PythonJavaClass, autoclass, java_method

# AndroidX classes for permission handling
ContextCompat = autoclass("androidx.core.content.ContextCompat")
ActivityCompat = autoclass("androidx.core.app.ActivityCompat")

# App specific classes
PythonActivity = autoclass("org.kivy.android.PythonActivity")
# Permission related classes
PackageManager = autoclass("android.content.pm.PackageManager")
Manifest = autoclass("android.Manifest")

# Python Activity to attach to
current_activity = PythonActivity.mActivity


# Handle the permission result callback
class PythonActivityOverride(PythonJavaClass):
    __javainterfaces__ = ["org/kivy/android/PythonActivity"]
    __javacontext__ = "app"

    @java_method("(I[Ljava/lang/String;[I)V")
    def onRequestPermissionsResult(self, requestCode, permissions, grantResults):
        if requestCode == 1:  # Ensure this matches the request code
            for i in range(len(grantResults)):
                if grantResults[i] == PackageManager.PERMISSION_GRANTED:
                    logging.info(f"Permission granted for {permissions[i]}")
                else:
                    logging.error(f"Permission denied for {permissions[i]}")


# Assign the custom class to override default PythonActivity behavior
override = PythonActivityOverride()


# Helper function to check and request permissions using AndroidX
def check_and_request_permissions(permissions: list) -> bool:
    permissions_to_request = []

    for permission in permissions:
        # Use ContextCompat to check permission status
        if (
            ContextCompat.checkSelfPermission(current_activity, permission)
            != PackageManager.PERMISSION_GRANTED
        ):
            permissions_to_request.append(permission)

    if permissions_to_request:
        # Use ActivityCompat to request permissions
        ActivityCompat.requestPermissions(current_activity, permissions_to_request, 1)
        return False
    return True


# The rest of your permission request functions can stay the same


def request_camera_permission():
    return check_and_request_permissions([Manifest.permission.CAMERA])


def request_location_permission():
    return check_and_request_permissions(
        [
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION,
        ]
    )


def request_storage_permission():
    return check_and_request_permissions(
        [
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
        ]
    )


def request_microphone_permission():
    return check_and_request_permissions([Manifest.permission.RECORD_AUDIO])


def request_bluetooth_permission():
    return check_and_request_permissions(
        [
            Manifest.permission.BLUETOOTH,
            Manifest.permission.BLUETOOTH_ADMIN,
            # Bluetooth permissions for Android 12 and above
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.BLUETOOTH_ADVERTISE,
            Manifest.permission.BLUETOOTH_CONNECT,
        ]
    )


def request_contacts_permission():
    return check_and_request_permissions(
        [Manifest.permission.READ_CONTACTS, Manifest.permission.WRITE_CONTACTS]
    )


def request_calendar_permission():
    return check_and_request_permissions(
        [Manifest.permission.READ_CALENDAR, Manifest.permission.WRITE_CALENDAR]
    )


def request_sms_permission():
    return check_and_request_permissions(
        [
            Manifest.permission.SEND_SMS,
            Manifest.permission.RECEIVE_SMS,
            Manifest.permission.READ_SMS,
        ]
    )


def request_phone_permission():
    return check_and_request_permissions(
        [
            Manifest.permission.CALL_PHONE,
            Manifest.permission.READ_PHONE_STATE,
            Manifest.permission.ANSWER_PHONE_CALLS,  # For Android 8.0 and above
        ]
    )


def request_sensors_permission():
    return check_and_request_permissions([Manifest.permission.BODY_SENSORS])


def request_wifi_permission():
    return check_and_request_permissions(
        [Manifest.permission.ACCESS_WIFI_STATE, Manifest.permission.CHANGE_WIFI_STATE]
    )


def request_all_permissions():
    request_camera_permission()
    request_location_permission()
    request_storage_permission()
    request_microphone_permission()
    request_bluetooth_permission()
    request_contacts_permission()
    request_calendar_permission()
    request_sms_permission()
    request_phone_permission()
    request_sensors_permission()
    request_wifi_permission()
