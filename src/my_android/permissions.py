import logging

from jnius import PythonJavaClass, autoclass, java_method

# App-specific classes
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


# Helper function to check and request permissions using Android's native API
def check_and_request_permissions(permissions: list) -> bool:
    permissions_to_request = []

    for permission in permissions:
        # Use PackageManager to check permission status directly
        if (
            current_activity.checkSelfPermission(permission)
            != PackageManager.PERMISSION_GRANTED
        ):
            permissions_to_request.append(permission)

    if permissions_to_request:
        # Request permissions using native API from the Activity
        current_activity.requestPermissions(permissions_to_request, 1)
        return False
    return True


# Define specific permission request functions
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


# You can add more permission functions as needed


def request_all_permissions():
    request_camera_permission()
    request_location_permission()
    request_storage_permission()
    request_microphone_permission()
