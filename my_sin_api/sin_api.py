import warnings
from requests import get, post, put, delete as delet


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
            if self.__class__.__name__ == '__Player':
                data['telegram_id'], data['owner_id'] = self.player_id, None
            put(self.post_url, headers=self.headers, json=data)
        else:
            self.__dict__[name] = value

    def __get(self, name):
        if name in self.__params:
            return get(self.get_url + name, headers=self.headers).json()[0]
        elif name in self.__dict__:
            return self.__dict__[name]


class SinApi:
    def __init__(self, api_key, api_url):
        self.__api_key = api_key
        self.__headers = {"Authorization": f"Bearer {self.__api_key}"}
        self.__api_url = api_url

    def mine(self, user_id):
        return self.__Mine(user_id, self.__api_key, self.__api_url)

    def player(self, user_id):
        return self.__Player(user_id, self.__api_key, self.__api_url)

    def factory(self, owner_id):
        return self.__Factory(owner_id, self.__api_key, self.__api_url)

    def find_factory(self, name):
        req = get(f'{self.__api_url}findFactory/{name}',
                  headers=self.__headers).text
        return self.factory(req) if req != '0' else req

    def stock(self):
        return get(f'{self.__api_url}stock',
                   headers=self.__headers).json()[0]

    def league_update(self):
        post(f'{self.__api_url}leagueUpdate', headers=self.__headers,
             allow_redirects=True)

    def lottery_start(self):
        return get(f'{self.__api_url}startLottery', headers=self.__headers).json()

    def reset_tickets(self):
        post(f'{self.__api_url}resetTickets', headers=self.__headers)

    class __Player(BaseClass):
        def __init__(self, user_id, api_key, api_url):
            try:
                int(user_id)
            except:
                user_id = get(f'{api_url}findUser/{user_id.replace('@', '')}',
                              headers={"Authorization": f"Bearer {api_key}"}).text
            super().__init__(user_id, api_key, api_url)

        def __str__(self):
            user_data = self.get('name,money,stolar,rating,league,clan_name,id,titles')
            _text = f"""
🌟*{user_data[0]}*🌟

💲 *Баланс:* {user_data[1]:,}
⚔️ *Столар:* {user_data[2]:,}

🏆 *Рейтинг:* {user_data[3]:,}
🛡️ *Лига:* {user_data[4]}

🌎 *Oбъединение:* {user_data[5].replace('_', ' ')}

*Идентификатор*: {user_data[6]}
                """
            title = user_data[7]
            if title:
                _text += f'\n\n🏆 *Титулы:* \n'
                for name in title.split():
                    _text += f"- {name.replace('_', ' ')}\n"
            return _text

        async def create(self, username: str, user: str):
            post(self.post_url, headers=self.headers,
                 json={"telegram_id": self.player_id, 'username': username, 'user': user})

        @property
        def exist(self) -> bool:
            try:
                return self.telegram_id == int(self.player_id)
            except:
                pass
            return False

        @property
        def is_banned(self) -> bool:
            return False

    class __Factory(BaseClass):

        def __str__(self):
            factory_data = self.get('name,lvl,state,tax,workers,ecology,stock,verification')
            return f"""
🏭 *{factory_data[0].replace('_', ' ')}*
🔧 *Уровень:* {factory_data[1]}
⚙️ *Тип:* {self.type}
🚧 *Статус:* {'Работает' if factory_data[2] == 1 else 'Не работает'}
💸 *Налоги:* {factory_data[3]}
👷‍ *Работники:* {factory_data[4]}
♻️ *Вклад в экологию:* {factory_data[5]}
📦 *Товара на складе:* {factory_data[6]}
{'🔎 _Знак качества_' if factory_data[7] == 1 else ''}
                        """

        @property
        def type(self):
            lvl = self.lvl
            if lvl >= 1000:
                return 'Звездная энергия'
            elif lvl >= 500:
                return 'Атомная энергия'
            elif lvl >= 100:
                return 'Солнечная энергия'
            elif lvl >= 50:
                return 'Химикаты'
            elif lvl >= 10:
                return 'Железо'
            else:
                return 'Древесина'

        @property
        def exist(self) -> bool:
            try:
                req = get(self.get_url + 'owner_id', headers=self.headers)
                return req.status_code != 404
            except:
                pass
            return False

        def create(self, name: str):
            post(self.post_url, headers=self.headers, json={'owner_id': self.player_id, 'name': name})

        def delete(self):
            delet(self.post_url, headers=self.headers, params={'owner_id': self.owner_id})

        def exists(self) -> bool:
            warnings.warn('This are going to be deleted, and replaced with __Factory.exist',
                          PendingDeprecationWarning, stacklevel=2)
            return self.exist

    class __Mine(BaseClass):

        def __str__(self):
            data = self.get('name,lvl,tax')
            return f"""
Шахта *{data[0]}*

*Размер:* {data[1]}
*Налоги:* {data[2]:,}

Выберите действие:
    """

        def create(self, name: str):
            post(self.post_url, headers=self.headers,
                 json={"owner_id": self.player_id, 'name': name})

        @property
        def exist(self):
            try:
                return self.owner_id == int(self.player_id)
            except:
                pass
            return False

        class Tunnel(BaseClass):

            def __str__(self):
                mine_id, tunnel_id, lvl, workers, eq, work = self.get('mine_id,id,lvl,workers,equipment,working')
                return f"""
Туннель № {f'{(mine_id - 100000) * tunnel_id:,}'.replace(',', '-')}
_Внутренний номер {tunnel_id:,}_

Работа: {'Приостановлена' if work == 0 else 'Идет полным ходом'}

Глубина: {lvl} километров.
Рабочие: {workers} человек.
"""
