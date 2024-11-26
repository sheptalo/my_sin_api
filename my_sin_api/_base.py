from requests.sessions import Session


class BaseClass:
    def __init__(self, user_id, api_key, api_url, ssl_verify):
        self.__dict__["player_id"] = str(user_id)
        self.__dict__["get_url"] = (
            f"{api_url}{self.__class__.__name__}/{user_id}/"
        )
        self.__dict__["post_url"] = f"{api_url}{self.__class__.__name__}"
        session = Session()
        session.headers.update({"Authorization": f"Bearer {api_key}"})
        session.verify = ssl_verify
        self.__dict__["session"] = session

    def __getitem__(self, name):
        return self.__get(name)

    def __getattr__(self, name):
        return self.__get(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def __setitem__(self, name, value):
        self.__set(name, value)

    def set(self, values: dict):
        self.session.put(self.get_url, json=values)

    def get(self, values: str):
        return self.session.get(self.get_url + values).json()

    def __set(self, name, value):
        self.session.put(self.get_url, json={name: value})

    def __get(self, name):
        res = self.session.get(self.get_url + name).json()
        if isinstance(res, list):
            return res[0]
        return res
