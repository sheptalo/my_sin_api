import warnings

from requests import get, post, delete as delet

from my_sin_api._base import BaseClass


class Player(BaseClass):
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


class Factory(BaseClass):

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


class Mine(BaseClass):

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
