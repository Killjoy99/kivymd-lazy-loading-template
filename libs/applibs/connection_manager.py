import logging

from httpx import Client, ConnectError

client = Client()


def get_google(client: Client):
    try:
        response = client.get("https://entweni.onrender.com")
        return response
    except ConnectError:
        logging.warning("Failed to Create a network.")
        return
