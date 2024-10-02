from jnius import autoclass, java_method, PythonJavaClass
import logging

# App specific classes
PythonActivity = autoclass("org.kivy.android.PythonActivity")
# Permission related classes
PackageManager = autoclass("android.content.pm.PackageManager")
Manifest = autoclass("android.Manifest")

Intent = autoclass("android.content.Intent")
Uri = autoclass("android.net.Uri")

# Handle the permission result callback
class PermissionCallback(PythonJavaClass):
    __javainterfaces__ = ['android/app/Activity$OnRequestPermissionsResultCallback']
    __javacontext__ = 'app'

    @java_method('(I[Ljava/lang/String;[I)V')
    def onRequestPermissionsResult(self, request_code, permissions, grant_results):
        if grant_results and grant_results[0] == PackageManager.PERMISSION_GRANTED:
            logging.info("Permission granted")
        else:
            logging.error("Permission denied")

permission_callback = PermissionCallback()

# Helper function to check and request permissions
def check_and_request_permissions(permissions: list) -> bool:
    current_activity = PythonActivity.mActivity
    permissions_to_request = []

    for permission in permissions:
        if current_activity.checkSelfPermission(permission) != PackageManager.PERMISSION_GRANTED:
            permissions_to_request.append(permission)
    
    if permissions_to_request:
        current_activity.requestPermissions(permissions_to_request, 1)
        return False
    return True

def request_camera_permission():
    return check_and_request_permissions([Manifest.permission.CAMERA])

def request_location_permission():
    return check_and_request_permissions([
        Manifest.permission.ACCESS_FINE_LOCATION,
        Manifest.permission.ACCESS_COARSE_LOCATION
    ])

def request_storage_permission():
    return check_and_request_permissions([
        Manifest.permission.READ_EXTERNAL_STORAGE,
        Manifest.permission.WRITE_EXTERNAL_STORAGE
    ])

def request_microphone_permission():
    return check_and_request_permissions([Manifest.permission.RECORD_AUDIO])

def request_bluetooth_permission():
    return check_and_request_permissions([
        Manifest.permission.BLUETOOTH,
        Manifest.permission.BLUETOOTH_ADMIN,
        # Bluetooth permissions for Android 12 and above
        Manifest.permission.BLUETOOTH_SCAN,
        Manifest.permission.BLUETOOTH_ADVERTISE,
        Manifest.permission.BLUETOOTH_CONNECT
    ])

def request_contacts_permission():
    return check_and_request_permissions([Manifest.permission.READ_CONTACTS, Manifest.permission.WRITE_CONTACTS])

def request_calendar_permission():
    return check_and_request_permissions([Manifest.permission.READ_CALENDAR, Manifest.permission.WRITE_CALENDAR])

def request_sms_permission():
    return check_and_request_permissions([
        Manifest.permission.SEND_SMS,
        Manifest.permission.RECEIVE_SMS,
        Manifest.permission.READ_SMS
    ])

def request_phone_permission():
    return check_and_request_permissions([
        Manifest.permission.CALL_PHONE,
        Manifest.permission.READ_PHONE_STATE,
        Manifest.permission.ANSWER_PHONE_CALLS  # For Android 8.0 and above
    ])

def request_sensors_permission():
    return check_and_request_permissions([Manifest.permission.BODY_SENSORS])

def request_wifi_permission():
    return check_and_request_permissions([
        Manifest.permission.ACCESS_WIFI_STATE,
        Manifest.permission.CHANGE_WIFI_STATE
    ])

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

