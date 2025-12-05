# Объект корабля игрока.
# Название корабль довольно расплывчатое, поскольку оно будет хранить не только данные игрока, но и игровую локацию в целом.
class Ship:

    # Инициализация объекта
    def __init__(self, user_ship_name: str):
        self.ship_name = user_ship_name  # Название корабля
        self.level = 0  # Уровень корабля 0 - 3
        self.strength = 100  # Прочность корабля 0 - 100
        self.crew_health = 100  # Здоровье экипажа 0 - 100
        self.speed = 100  # Скорость корабля
        self.fuel = 100  # Уровень топлива 0 - 100
        self.oxygen = 100  # Уровень кислорода 0 - 100
        self.resources = 300 # Ресурсы
        self.day = 0 # Количество прожитых дней.
        self.on_planet = False  # Корабль находится на планете?
        self.planet_id = -1  # ID планеты, на которой находится корабль. Если -1, значит корабль не находится на планете (см. выше)
        self.actions_blocked = False  # Действия игроков заблокированы?

    # Экспортирует этот объект в виде словаря, для удобного сохранения в json.
    def export_as_dict(self) -> dict:
        ex_dict = {
            'ship_name': self.ship_name,
            'level': self.level,
            'strength': self.strength,
            'crew_health': self.strength,
            'speed': self.speed,
            'fuel': self.fuel,
            'oxygen': self.oxygen,
            'resources' : self.resources,
            'day': self.day,
            'on_planet': self.on_planet,
            'planet_id': self.planet_id,
            'actions_blocked': self.actions_blocked
        }
        return ex_dict

    # Применяет значения из словаря.
    def import_from_dict(self, imported_ship: dict):
        try:
            self.ship_name = imported_ship['ship_name']
            self.level = imported_ship['level']
            self.strength = imported_ship['strength']
            self.crew_health = imported_ship['crew_health']
            self.speed = imported_ship['speed']
            self.fuel = imported_ship['fuel']
            self.oxygen = imported_ship['oxygen']
            self.resources = imported_ship['resources']
            self.day = imported_ship['day']
            self.on_planet = imported_ship['on_planet']
            self.planet_id = imported_ship['planet_id']
            self.actions_blocked = imported_ship['actions_blocked']
        except KeyError as e:
            print(f"[E] Не удалось импортировать какие-то данные из JSON. Возможно, файл устарел. Детали: {e}")
        return self
