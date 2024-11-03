from requests import get, put


class BaseClass:
    __params = []

    def __new__(cls, user_id, api_key, api_url):
        if not cls.__params:
            cls.__params = get(api_url + 'params').json() + ['tunnels']
        self = super().__new__(cls)
        return self

    def __init__(self, user_id, api_key, api_url):
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.player_id = str(user_id)
        self.get_url = f"{api_url}{self.__class__.__name__.replace('__', '')}/{user_id}/"
        self.post_url = f"{api_url}{self.__class__.__name__.replace('__', '')}"

    def __getitem__(self, name):
        return self.__get(name)

    def __getattr__(self, name):
        return self.__get(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def __setitem__(self, name, value):
        self.__set(name, value)

    def set(self, values: dict):
        put(self.post_url, json=values, headers=self.headers)

    def get(self, values: str):
        return get(self.get_url + values, headers=self.headers).json()

    def __set(self, name, value):
        if name in self.__params:
            data = {'owner_id': str(self.player_id), name: value}
            if self.__class__.__name__ == 'Player':
                data['telegram_id'], data['owner_id'] = self.player_id, None
            put(self.post_url, headers=self.headers, json=data)
        else:
            self.__dict__[name] = value

    def __get(self, name):
        if name in self.__params:
            return get(self.get_url + name, headers=self.headers).json()[0]
        elif name in self.__dict__:
            return self.__dict__[name]
