# Объект корабля игрока.
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
        self.inside_temperature = 36 # Температура внутри корабля
        self.outside_temperature = 0  # Температура вне корабля
        self.resources = 300  # Ресурсы
        self.day = 0  # Количество прожитых дней.
        self.on_planet = False  # Корабль находится на планете?
        self.planet_id = -1  # ID планеты, на которой находится корабль. Если -1, значит корабль не находится на планете (см. выше)
        self.actions_blocked = False  # Действия игроков заблокированы?
        # Модули корабля
        self.module_main_engine_health = 100  # Прочность главного двигателя.
        self.module_fuel_tank_health = 100  # Прочность топливного бака.
        self.module_cooling_system_health = 100  # Прочность систем охлаждения.
        self.module_life_support_health = 100  # Прочность системы жизнеобеспечения.
        self.module_command_bridge_health = 100  # Прочность капитанского мостика.
        self.module_computer_health = 100  # Прочность бортового компьютера.
        self.module_weapon_health = 100  # Прочность орудия.

    # Экспортирует этот объект в виде словаря, для удобного сохранения в json.
    def export_as_dict(self) -> dict:
        return {
            'ship_name': self.ship_name,
            'level': self.level,
            'strength': self.strength,
            'crew_health': self.strength,
            'speed': self.speed,
            'fuel': self.fuel,
            'oxygen': self.oxygen,
            'inside_temperature': self.inside_temperature,
            'outside_temperature': self.outside_temperature,
            'resources': self.resources,
            'day': self.day,
            'on_planet': self.on_planet,
            'planet_id': self.planet_id,
            'actions_blocked': self.actions_blocked,
            'module_main_engine_health': self.module_main_engine_health,
            'module_fuel_tank_health': self.module_fuel_tank_health,
            'module_cooling_system_health': self.module_cooling_system_health,
            'module_life_support_health': self.module_life_support_health,
            'module_command_bridge_health': self.module_command_bridge_health,
            'module_computer_health': self.module_computer_health,
            'module_weapon_health': self.module_weapon_health
        }

    # Применяет значения из словаря.
    def import_from_dict(self, imported_ship: dict):
        try:
            self.ship_name = imported_ship['ship_name']
            self.level = imported_ship['level']

            self.strength = imported_ship['strength']
            if self.strength > 100 or self.strength < 0:
                print(f"[W] Неправильное значение переменной strength, сброс до значений по умолчанию.")
                self.strength = 100

            self.crew_health = imported_ship['crew_health']
            if self.crew_health > 100 or self.crew_health < 0:
                print(f"[W] Неправильное значение переменной strength, сброс до значений по умолчанию.")
                self.crew_health = 100
            self.speed = imported_ship['speed']

            self.fuel = imported_ship['fuel']
            if self.fuel > 100 or self.fuel < 0:
                print(f"[W] Неправильное значение переменной fuel, сброс до значений по умолчанию.")
                self.fuel = 100

            self.oxygen = imported_ship['oxygen']
            if self.oxygen > 100 or self.oxygen < 0:
                print(f"[W] Неправильное значение переменной oxygen, сброс до значений по умолчанию.")
                self.oxygen = 100

            self.inside_temperature = imported_ship['inside_temperature']
            self.outside_temperature = imported_ship['outside_temperature']
            self.resources = imported_ship['resources']
            self.day = imported_ship['day']
            self.on_planet = imported_ship['on_planet']
            self.planet_id = imported_ship['planet_id']
            self.actions_blocked = imported_ship['actions_blocked']
            self.module_main_engine_health = imported_ship['module_main_engine_health']
            self.module_fuel_tank_health = imported_ship['module_fuel_tank_health']
            self.module_cooling_system_health = imported_ship['module_cooling_system_health']
            self.module_life_support_health = imported_ship['module_life_support_health']
            self.module_command_bridge_health = imported_ship['module_command_bridge_health']
            self.module_computer_health = imported_ship['module_computer_health']
            self.module_weapon_health = imported_ship['module_weapon_health']
        except KeyError as e:
            print(f"[E] Не удалось импортировать какие-то данные из JSON. Возможно, файл устарел. Детали: {e}")
        return self
