from requests import get, put


class BaseClass:

    def __init__(self, user_id, api_key, api_url):
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.uid = str(user_id)
        self.get_url = f"{api_url}{self.__class__.__name__}/{user_id}/"
        self.post_url = f"{api_url}{self.__class__.__name__}"

    def __getitem__(self, name):
        return self.__get(name)

    def __getattr__(self, name):
        return self.__get(name)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def __setitem__(self, name, value):
        self.__set(name, value)

    def set(self, values: dict):
        put(self.get_url, json=values, headers=self.headers)

    def get(self, values: str):
        return get(self.get_url + values, headers=self.headers).json()

    def __set(self, name, value):
        if name in self.__params:
            put(self.get_url, headers=self.headers, json={name: value})
        else:
            self.__dict__[name] = value

    def __get(self, name):
        if name in self.__params:
            return get(self.get_url + name, headers=self.headers).json()[0]
        elif name in self.__dict__:
            return self.__dict__[name]
