from jnius import autoclass

# Access Android Java classes via pyjnius
PythonActivity = autoclass("org.kivy.android.PythonActivity")
ActivityCompat = autoclass("android.support.v4.app.ActivityCompat")
ContextCompat = autoclass("android.support.v4.content.ContextCompat")
PackageManager = autoclass("android.content.pm.PackageManager")
Manifest = autoclass("android.Manifest")


def check_permissions() -> bool:
    # Get the current activity
    current_activity = PythonActivity.mActivity
    permission = Manifest.permission.CAMERA
    # Check if permission is granted
    return (
        ContextCompat.checkSelfPermission(current_activity, permission)
        == PackageManager.PERMISSION_GRANTED
    )


def request_permissions() -> None:
    if not check_permissions():
        current_activity = PythonActivity.mActivity
        permission = Manifest.permission.CAMERA
        # Request the necessary permission
        ActivityCompat.requestPermissions(current_activity, [permission], 1)


# Note: We do not need to manually handle the result in this minimal version.
# Android will handle the result, and you can access the status via `check_permissions()`.
