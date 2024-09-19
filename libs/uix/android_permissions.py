# Checking and requestion permissions during runtime

from android.permissions import Permission, check_permission, request_permissions


def has_required_permissions():
    """Check if the required permissions are already granted."""
    required_permissions = [
        Permission.CAMERA,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.RECORD_AUDIO,
    ]
    for permission in required_permissions:
        if not check_permission(permission):
            return False  # If any permission is missing, return False
    return True  # All permissions are granted


def check_and_request_permissions(on_permission_denied_callback):
    """Check for permissions and request if they are not granted. Show popup on denial."""
    if not has_required_permissions():
        # Request the permissions if they are not already granted
        def on_permissions_callback(permissions, grants):
            if not all(grants):
                # If any permission is denied, call the denial callback
                on_permission_denied_callback()

        request_permissions(
            [
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.RECORD_AUDIO,
            ],
            on_permissions_callback,
        )
    else:
        print("All permissions are already granted.")
