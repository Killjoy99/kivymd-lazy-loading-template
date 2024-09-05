import logging

from httpx import Client, ConnectError

client = Client()


class ConnectionManager:
    def __init__(self, client: Client) -> None:
        self.client = client

    def get_google(self):
        try:
            response = client.get("https://google.com")
            return response
        except ConnectError:
            logging.warning("Failed to Create a network.")
            return
