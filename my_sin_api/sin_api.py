from requests import get, post

from my_sin_api._base import BaseClass
from my_sin_api._models import Player, Factory, Mine, Tunnel


class SinApi:
    """Base class for all Sin APIs."""

    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.api_url = api_url

    def any(self, name, some_id):
        """creates class to fast use your api"""
        a = type(name, (BaseClass,), {})
        return a(some_id, self.api_key, self.api_url)

    # region Tegtory Functions
    def mine(self, user_id):
        """returns mine of given user."""
        return Mine(user_id, self.api_key, self.api_url)

    def player(self, user_id):
        """returns player of given user_id."""
        return Player(user_id, self.api_key, self.api_url)

    def factory(self, owner_id):
        """returns factory of given owner."""
        return Factory(owner_id, self.api_key, self.api_url)

    def tunnel(self, tunnel_id):
        """returns tunnel of given tunnel_id."""
        return Tunnel(tunnel_id, self.api_key, self.api_url)

    def find_factory(self, name):
        req = get(f'{self.api_url}findFactory/{name}',
                  headers=self.headers).text
        return self.factory(req) if req != '0' else req

    def stock(self):
        return get(f'{self.api_url}stock',
                   headers=self.headers).json()[0]

    def league_update(self):
        post(f'{self.api_url}leagueUpdate', headers=self.headers,
             allow_redirects=True)

    def lottery_start(self):
        return get(f'{self.api_url}startLottery', headers=self.headers).json()

    def reset_tickets(self):
        post(f'{self.api_url}resetTickets', headers=self.headers)
    # endregion
