from requests import get
from my_sin_api._base import BaseClass


class Tegtory(BaseClass):
    __params = []

    def __new__(cls, user_id, api_key, api_url, ssl_verify):
        if not cls.__params:
            cls.__params = get(api_url + "params", verify=ssl_verify).json()
        self = super().__new__(cls)
        return self

    def __init__(self, user_id, api_key, api_url, ssl_verify):
        super().__init__(user_id, api_key, api_url, ssl_verify)
        self.__dict__["api_url"] = api_url

    def get_stock(self):
        return self.session.get(f"{self.api_url}stock").json()[0]

    def league_update(self):
        self.session.post(f"{self.api_url}leagueUpdate", allow_redirects=True)

    def lottery_start(self):
        return self.session.get(f"{self.api_url}startLottery").json()

    def reset_tickets(self):
        self.session.post(f"{self.api_url}resetTickets")


class Player(Tegtory):
    def __init__(self, user_id, api_key, api_url, ssl_verify):
        try:
            int(user_id)
        except:
            user_id = get(
                f'{api_url}findUser/{user_id.replace('@', '')}',
                headers={"Authorization": f"Bearer {api_key}"},
                verify=ssl_verify,
            ).text
        super().__init__(user_id, api_key, api_url, ssl_verify)

    def __str__(self):
        user_data = self.get(
            "name,money,stolar,rating,league,clan_name,id,titles"
        )
        _text = f"""
🌟*{user_data[0]}*🌟

💲 *Баланс:* {user_data[1]:,}
⚔️ *SC:* {user_data[2]:,}

🏆 *Рейтинг:* {user_data[3]:,}
🛡️ *Лига:* {user_data[4]}

🌎 *Oбъединение:* {user_data[5].replace('_', ' ')}

*Идентификатор*: {user_data[6]}
                """
        title = user_data[7]
        if title:
            _text += "\n\n🏆 *Титулы:* \n"
            for name in title.split():
                _text += f"- {name.replace('_', ' ')}\n"
        return _text

    async def create(self, username: str, user: str):
        self.session.post(
            self.post_url,
            json={
                "telegram_id": self.player_id,
                "username": username,
                "name": user,
            },
        )

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


class Factory(Tegtory):
    def __str__(self):
        factory_data = self.get(
            "name,lvl,state,tax,workers,ecology,stock,verification"
        )
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
            return "Звездная энергия"
        elif lvl >= 500:
            return "Атомная энергия"
        elif lvl >= 100:
            return "Солнечная энергия"
        elif lvl >= 50:
            return "Химикаты"
        elif lvl >= 10:
            return "Железо"
        else:
            return "Древесина"

    @property
    def exist(self) -> bool:
        try:
            req = self.session.get(self.get_url + "owner_id")
            return req.status_code != 404
        except:
            pass
        return False

    def create(self, name: str):
        self.session.post(
            self.post_url, json={"owner_id": self.player_id, "name": name}
        )

    def delete(self):
        self.session.delete(self.post_url, params={"owner_id": self.owner_id})
