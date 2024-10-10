import logging

from kivy.properties import ListProperty
from kivy.utils import platform
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

logger = logging.getLogger(__name__)


class MessagingScreen(MDScreen):
    messages = ListProperty([])  # List of messages to display

    def on_enter(self):
        if platform == "android":
            self.request_sms_permissions()
            self.messages = self.read_sms_messages()
            self.update_recycle_view()  # Update the RecycleView with the messages

    def request_sms_permissions(self):
        try:
            from android.permissions import Permission, request_permissions

            def callback(permissions, results):
                for permission, result in zip(permissions, results):
                    if result:
                        logger.info(f"Permission granted: {permission}")
                    else:
                        logger.warning(f"Permission denied: {permission}")

            request_permissions([Permission.READ_SMS], callback)
        except Exception as e:
            logger.error(f"Error requesting for permission: {e}")

    def read_sms_messages(self):
        try:
            from jnius import autoclass

            Sms = autoclass("android.provider.Telephony$Sms")
            ContentResolver = autoclass("android.content.ContentResolver")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            current_activity = PythonActivity.mActivity

            # Query sms messages
            resolver = current_activity.getContentResolver()
            cursor = resolver.query(Sms.CONTENT_URI, None, None, None, None)

            if cursor is not None:
                sms_messages = []
                while cursor.moveToNext():
                    body = cursor.getString(cursor.getColumnIndex(Sms.BODY))
                    address = cursor.getString(cursor.getColumnIndex(Sms.ADDRESS))
                    sms_messages.append(f"From: {address}, Message: {body}")

                cursor.close()
                return sms_messages

        except Exception as e:
            logger.error(f"Error while reading sms messages: {e}")
            return []

    def update_recycle_view(self):
        # Update the RecycleView with the messages
        # self.ids.sms_recycle_view.data = [
        #     {"text": message} for message in self.messages
        # ]
        for i in range(10):
            self.ids.sms_recycle_view.add_widget(MDLabel(text=f"{i}"))
