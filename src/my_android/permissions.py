from jnius import autoclass

# App specific classes
PythonActivity = autoclass("org.kivy.android.PythonActivity")
# Permission related classes
PackageManager = autoclass("android.content.pm.PackageManager")
Manifest = autoclass("android.Manifest")

# Handle the permission result callback
def onRequestPermissionResult(request_code, permissions, grant_results):
    if grant_results and grant_results[0] == PackageManager.PERMISSION_GRANTED:
        # Permission granted
        print("Permission granted")
    else:
        # Permission denied
        print("Permission denied")

# Methods to check and request permissions
def check_and_request_permissions(permission: str) -> bool:
    current_activity = PythonActivity.mActivity
    # Check if permission is already granted
    if current_activity.checkSelfPermission(permission) != PackageManager.PERMISSION_GRANTED:
        # Permission not granted, request it
        current_activity.requestPermissions([permission], 1)
    else:
        # Permission already granted
        return True

def request_camera_permission():
    check_and_request_permissions(Manifest.permission.CAMERA)

def request_location_permission():
    check_and_request_permissions(Manifest.permission.ACCESS_FINE_LOCATION)
    check_and_request_permissions(Manifest.permission.ACCESS_COARSE_LOCATION)

def request_storage_permission():
    check_and_request_permissions(Manifest.permission.READ_EXTERNAL_STORAGE)
    check_and_request_permissions(Manifest.permission.WRITE_EXTERNAL_STORAGE)

def request_microphone_permission():
    check_and_request_permissions(Manifest.permission.RECORD_AUDIO)

def request_bluetooth_permission():
    check_and_request_permissions(Manifest.permission.BLUETOOTH)
    check_and_request_permissions(Manifest.permission.BLUETOOTH_ADMIN)
    # TODO: Add Bluetooth permissions for Android 12 and above
    # check_and_request_permissions(Manifest.permission.BLUETOOTH_SCAN)
    # check_and_request_permissions(Manifest.permission.BLUETOOTH_ADVERTISE)
    # check_and_request_permissions(Manifest.permission.BLUETOOTH_CONNECT)

def request_all_permissions():
    request_camera_permission()
    request_location_permission()
    request_storage_permission()
    request_microphone_permission()
    request_bluetooth_permission()

