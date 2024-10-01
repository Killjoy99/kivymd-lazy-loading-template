from android import activity  # noqa: F401
from jnius import JavaMethod, autoclass

# Access Android Java classes via pyjnius
Context = autoclass("android.content.Context")
ActivityCompat = autoclass("androidx.core.app.ActivityCompat")
PackageManager = autoclass("android.content.pm.PackageManager")
Manifest = autoclass("android.Manifest")


def check_permissions() -> bool:
    current_activity = activity.get_activity()
    permission = Manifest.permission.CAMERA
    # Check if permission is granted
    return (
        ActivityCompat.checkSelfPermission(current_activity, permission)
        == PackageManager.PERMISSION_GRANTED
    )


def request_permissions() -> None:
    if not check_permissions():
        current_activity = activity.get_activity()
        permission = Manifest.permission.CAMERA
        ActivityCompat.requestPermissions(current_activity, [permission], 1)


class MyActivityListener(activity.PythonActivity):
    onRequestPermissionsResult = JavaMethod(
        "int", "java.lang.String[]", "int[]", name="onRequestPermissionsResult"
    )

    def onRequestPermissionsResult(self, request_code, permissions, grant_results):
        super(MyActivityListener, self).onRequestPermissionsResult(
            request_code, permissions, grant_results
        )
        if request_code == 1:
            if grant_results[0] == PackageManager.PERMISSION_GRANTED:
                print("Permission granted")
            else:
                print("Permission denied")


activity.set_listener(MyActivityListener())
