from requests import get

from my_sin_api._base import BaseClass
from my_sin_api._models import Player, Factory


class SinApi:
    def __init__(self, api_key, api_url, *, ssl_verify=True):
        """
        Base class for all Sin APIs.

        :param ssl_verify: Check, verifies ssl on endpoint
        """
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.api_url = api_url
        self.ssl_verify = ssl_verify
        if not ssl_verify:
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def any(self, name, some_id):
        """creates class to fast use your api"""
        a = type(name, (BaseClass,), {})
        return a(some_id, self.api_key, self.api_url, self.ssl_verify)

    # region Tegtory Functions

    def player(self, user_id):
        """returns player of given user_id."""
        return Player(user_id, self.api_key, self.api_url, self.ssl_verify)

    def factory(self, owner_id):
        """returns factory of given owner."""
        return Factory(owner_id, self.api_key, self.api_url, self.ssl_verify)

    def find_factory(self, name):
        req = get(
            f"{self.api_url}findFactory/{name}", headers=self.headers
        ).text
        return self.factory(req) if req != "0" else req

    # endregion
