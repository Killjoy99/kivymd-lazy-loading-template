import logging

from httpx import AsyncClient, ConnectError

client = AsyncClient()


class ConnectionManager:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    def get_google(self):
        try:
            response = client.get("https://google.com")
            return response
        except ConnectError:
            logging.warning("Failed to Create a network.")
            return
