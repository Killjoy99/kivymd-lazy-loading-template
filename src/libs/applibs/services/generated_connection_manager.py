
import httpx

from libs.applibs.utils import load_cookies, save_cookies  # noqa: F401

online_server_url = "https://embakweaziwe.onrender.com"
server_url = "http://127.0.0.1:8000"

# Create a Client instance with cookies
def create_client():
    # create a client session (client = create_client()) to use for that session (app lifetime)
    cookies = load_cookies()
    return httpx.Client(cookies=cookies)


class HomeRoutes:
    def __init__(self, client):
        self.client = client

    def index__get(self, **kwargs):
        response =  self.client.get(f'{server_url}/', follow_redirects=True, **kwargs)

        return response

    def index__get(self, **kwargs):
        response =  self.client.get(f'{server_url}/', follow_redirects=True, **kwargs)

        return response

    def healthcheck_healthcheck_get(self, **kwargs):
        response =  self.client.get(f'{server_url}/healthcheck', follow_redirects=True, **kwargs)

        return response

    def healthcheck_healthcheck_get(self, **kwargs):
        response =  self.client.get(f'{server_url}/healthcheck', follow_redirects=True, **kwargs)

        return response

    def microservices_home_microservices_get(self, **kwargs):
        response =  self.client.get(f'{server_url}/microservices', follow_redirects=True, **kwargs)

        return response


class AuthRoutes:
    def __init__(self, client):
        self.client = client

    def register_user_auth_register_post(self, **kwargs):
        '''
        Expected data: application/json
        Schema: {'$ref': '#/components/schemas/UserCreate'}
        '''
        response =  self.client.post(f'{server_url}/auth/register', follow_redirects=True, **kwargs)

        return response

    def authenticate_user_auth_login_post(self, **kwargs):
        '''
        Expected data: application/x-www-form-urlencoded
        Schema: {'$ref': '#/components/schemas/Body_authenticate_user_auth_login_post'}
        '''
        response =  self.client.post(f'{server_url}/auth/login', follow_redirects=True, **kwargs)

        return response

    def refresh_access_token_auth_refresh_post(self, **kwargs):
        response =  self.client.post(f'{server_url}/auth/refresh', follow_redirects=True, **kwargs)

        return response

    def get_loged_in_user_auth_me_get(self, **kwargs):
        response =  self.client.get(f'{server_url}/auth/me', follow_redirects=True, **kwargs)

        return response


class BookingRoutes:
    def __init__(self, client):
        self.client = client

    def booking_home_booking_get(self, **kwargs):
        response =  self.client.get(f'{server_url}/booking', follow_redirects=True, **kwargs)

        return response

    def create_booking_booking_bookings_post(self, **kwargs):
        response =  self.client.post(f'{server_url}/booking/bookings', follow_redirects=True, **kwargs)

        return response


class School_managementRoutes:
    def __init__(self, client):
        self.client = client

    def school_home_school_management_get(self, **kwargs):
        response =  self.client.get(f'{server_url}/school_management', follow_redirects=True, **kwargs)

        return response


