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
        self.inside_temperature = 25  # Температура внутри корабля
        self.outside_temperature = -260  # Температура вне корабля
        self.resources = 300  # Ресурсы
        self.day = 0  # Количество прожитых дней.
        self.on_planet = False  # Корабль находится на планете?
        self.planet_id = -1  # ID планеты, на которой находится корабль. Если -1, значит корабль не находится на планете (см. выше)
        self.visited_planets: list[int] = []  # ID планет, на которых игрок уже побывал.
        # Модули корабля
        self.module_main_engine_damaged = False  # Статус главного двигателя.
        self.module_fuel_tank_damaged = False  # Статус топливного бака.
        self.module_cooling_system_damaged = False  # Статус систем охлаждения двигателя.
        self.module_life_support_damaged = False  # Статус системы жизнеобеспечения.
        self.module_computer_damaged = False  # Статус бортового компьютера.
        self.module_weapon_damaged = False  # Статус орудия.

    # Вернёт True, если повреждены все модули корабля.
    def are_all_system_damaged(self) -> bool:
        return (self.module_main_engine_damaged and self.module_fuel_tank_damaged and self.module_cooling_system_damaged
                and self.module_life_support_damaged and self.module_computer_damaged and self.module_weapon_damaged)

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
            'visited_planets': self.visited_planets,
            'module_main_engine_damaged': self.module_main_engine_damaged,
            'module_fuel_tank_damaged': self.module_fuel_tank_damaged,
            'module_cooling_system_damaged': self.module_cooling_system_damaged,
            'module_life_support_damaged': self.module_life_support_damaged,
            'module_computer_damaged': self.module_computer_damaged,
            'module_weapon_damaged': self.module_weapon_damaged
        }

    # Применяет значения из словаря.
    def import_from_dict(self, imported_ship: dict):
        try:
            self.ship_name = imported_ship['ship_name']
            # Название корабля должно быть больше 3 и менее 16 символов.
            if len(self.ship_name) < 3 or len(self.ship_name) > 15:
                print(f"[W] Неправильная длина названия корабля, сброс до значений по умолчанию.")
                self.ship_name = "ERROR"

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
            self.visited_planets = imported_ship['visited_planets']
            self.module_main_engine_damaged = imported_ship['module_main_engine_damaged']
            self.module_fuel_tank_damaged = imported_ship['module_fuel_tank_damaged']
            self.module_cooling_system_damaged = imported_ship['module_cooling_system_damaged']
            self.module_life_support_damaged = imported_ship['module_life_support_damaged']
            self.module_computer_damaged = imported_ship['module_computer_damaged']
            self.module_weapon_damaged = imported_ship['module_weapon_damaged']
        except KeyError as e:
            print(f"[E] Не удалось импортировать какие-то данные из JSON. Возможно, файл устарел. Детали: {e}")
        return self
