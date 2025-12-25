import random

import colorama

from base.core import components
from base.core.clamp import clamp


# Класс события на планете
class PlanetEvent:

    # Возвращает цвет текста
    @staticmethod
    def get_text_color(value: str) -> str:
        match value:
            case "red":
                return colorama.Fore.RED
            case "cyan":
                return colorama.Fore.CYAN
            case "yellow":
                return colorama.Fore.YELLOW

            # Зеленый - цвет по умолчанию
            case _:
                return colorama.Fore.GREEN

    def __init__(self, m_event_name: str, m_event_description: str, m_event_commands: list[str], m_prob: float,
                 m_color: str):
        self.event_name: str = m_event_name  # Название события, в игре пока что не используется, но это удобно создателям.
        self.event_description: str = m_event_description  # Описание события (то, что увидит игрок в Последних действиях)
        self.event_commands: list[str] = m_event_commands  # Команда(-ы) для генерации события(-ий).
        self.event_prob: float = m_prob  # Вероятность события (от 0.000 до 1.000)
        self.event_text_color: str = self.get_text_color(m_color)  # Цвет текста события.

    # Обработка команды
    def handle_event_command(self, command: list[str]):
        print(command)
        # Первый аргумент
        match command[0]:
            # Изменение ресурсов
            case "resources":
                # Второй аргумент
                match command[1]:
                    # Добавить ресурсы
                    case "add":
                        # Пробуем добавить ресурсы
                        try:
                            base_size = int(command[2])  # Базовое значение
                            var = int(command[3])  # Погрешность
                            # Изменяем
                            components.GAME.player.resources += random.randint(base_size - var, base_size + var)
                        except ValueError:
                            # Вероятно, ошибка при выполнении str -> int или str -> float
                            if components.SETTINGS.get_debug_mode():
                                print(
                                    f"В событии {self.event_name} не получилось преобразовать {command[2]} или {command[3]}. Проверьте правильность написания события.")
                    # Убавить ресурсы
                    case "remove":
                        # Пробуем убавить ресурсы
                        try:
                            base_size = int(command[2])  # Базовое значение
                            var = int(command[3])  # Погрешность
                            # Изменяем
                            components.GAME.player.resources = clamp(
                                components.GAME.player.resources - random.randint(base_size - var, base_size + var),
                                0,
                                99999)
                        except ValueError:
                            # Вероятно, ошибка при выполнении str -> int или str -> float
                            if components.SETTINGS.get_debug_mode():
                                print(
                                    f"В событии {self.event_name} не получилось преобразовать {command[2]} или {command[3]}. Проверьте правильность написания события.")
            # Изменение прочности корабля
            case "strength":
                # Второй аргумент
                match command[1]:
                    # Добавить прочность
                    case "add":
                        # Пробуем добавить прочность
                        try:
                            base_size = int(command[2])  # Базовое значение
                            var = int(command[3])  # Погрешность
                            # Изменяем
                            components.GAME.player.strength = clamp(
                                components.GAME.player.strength + random.randint(base_size - var, base_size + var),
                                0,
                                100)
                        except ValueError:
                            # Вероятно, ошибка при выполнении str -> int или str -> float
                            if components.SETTINGS.get_debug_mode():
                                print(
                                    f"В событии {self.event_name} не получилось преобразовать {command[2]} или {command[3]}. Проверьте правильность написания события.")
                    # Убавить прочность
                    case "remove":
                        # Пробуем убавить прочность
                        try:
                            base_size = int(command[2])  # Базовое значение
                            var = int(command[3])  # Погрешность
                            # Изменяем
                            components.GAME.player.strength = clamp(
                                components.GAME.player.strength - random.randint(base_size - var, base_size + var),
                                0,
                                100)
                        except ValueError:
                            # Вероятно, ошибка при выполнении str -> int или str -> float
                            if components.SETTINGS.get_debug_mode():
                                print(
                                    f"В событии {self.event_name} не получилось преобразовать {command[2]} или {command[3]}. Проверьте правильность написания события.")
            # Изменение здоровья экипажа
            case "crew":
                # Второй аргумент
                match command[1]:
                    # Добавить здоровье
                    case "add":
                        # Пробуем добавить здоровье
                        try:
                            base_size = int(command[2])  # Базовое значение
                            var = int(command[3])  # Погрешность
                            # Изменяем
                            components.GAME.player.crew_health = clamp(
                                components.GAME.player.crew_health + random.randint(base_size - var, base_size + var),
                                0,
                                100)
                        except ValueError:
                            # Вероятно, ошибка при выполнении str -> int или str -> float
                            if components.SETTINGS.get_debug_mode():
                                print(
                                    f"В событии {self.event_name} не получилось преобразовать {command[2]} или {command[3]}. Проверьте правильность написания события.")
                    # Убавить здоровье
                    case "remove":
                        # Пробуем убавить здоровье
                        try:
                            base_size = int(command[2])  # Базовое значение
                            var = int(command[3])  # Предел изменения
                            # Изменяем
                            components.GAME.player.crew_health = clamp(
                                components.GAME.player.crew_health - random.randint(base_size - var, base_size + var),
                                0,
                                100)
                        except ValueError:
                            # Вероятно, ошибка при выполнении str -> int или str -> float
                            if components.SETTINGS.get_debug_mode():
                                print(
                                    f"В событии {self.event_name} не получилось преобразовать {command[2]} или {command[3]}. Проверьте правильность написания события.")
            # Изменение уровня кислород
            case "oxygen":
                # Второй аргумент
                match command[1]:
                    # Добавить кислород
                    case "add":
                        # Пробуем добавить кислород
                        try:
                            base_size = int(command[2])  # Базовое значение
                            var = int(command[3])  # Погрешность
                            # Изменяем
                            components.GAME.player.oxygen = clamp(
                                components.GAME.player.oxygen + random.randint(base_size - var, base_size + var),
                                0,
                                100)
                        except ValueError:
                            # Вероятно, ошибка при выполнении str -> int или str -> float
                            if components.SETTINGS.get_debug_mode():
                                print(
                                    f"В событии {self.event_name} не получилось преобразовать {command[2]} или {command[3]}. Проверьте правильность написания события.")
                    # Убавить здоровье
                    case "remove":
                        # Пробуем убавить здоровье
                        try:
                            base_size = int(command[2])  # Базовое значение
                            var = int(command[3])  # Предел изменения
                            # Изменяем
                            components.GAME.player.oxygen = clamp(
                                components.GAME.player.oxygen - random.randint(base_size - var, base_size + var),
                                0,
                                100)
                        except ValueError:
                            # Вероятно, ошибка при выполнении str -> int или str -> float
                            if components.SETTINGS.get_debug_mode():
                                print(
                                    f"В событии {self.event_name} не получилось преобразовать {command[2]} или {command[3]}. Проверьте правильность написания события.")
            # Изменение модуля Двигатель
            case "module_engine":
                # Второй аргумент
                match command[1]:
                    # Починить модуль
                    case "1":
                        components.GAME.player.module_computer_damaged = False
                    # Повредить модуль
                    case "0":
                        components.GAME.player.module_computer_damaged = True
                    case _:
                        if components.SETTINGS.get_debug_mode():
                            print(f"Неизвестный аргумент {command[1]} события {self.event_name}")
            # Изменение модуля Топливный бак
            case "module_fuel_tank":
                # Второй аргумент
                match command[1]:
                    # Починить модуль
                    case "1":
                        components.GAME.player.module_fuel_tank_damaged = False
                    # Повредить модуль
                    case "0":
                        components.GAME.player.module_fuel_tank_damaged = True
                    case _:
                        if components.SETTINGS.get_debug_mode():
                            print(f"Неизвестный аргумент {command[1]} события {self.event_name}")
            # Изменение модуля Система охлаждения двигателя
            case "module_cooling_system":
                # Второй аргумент
                match command[1]:
                    # Починить модуль
                    case "1":
                        components.GAME.player.module_cooling_system_damaged = False
                    # Повредить модуль
                    case "0":
                        components.GAME.player.module_cooling_system_damaged = True
                    case _:
                        if components.SETTINGS.get_debug_mode():
                            print(f"Неизвестный аргумент {command[1]} события {self.event_name}")
            # Изменение модуля Система жизнеобеспечения
            case "module_life_support":
                # Второй аргумент
                match command[1]:
                    # Починить модуль
                    case "1":
                        components.GAME.player.module_life_support_damaged = False
                    # Повредить модуль
                    case "0":
                        components.GAME.player.module_life_support_damaged = True
                    case _:
                        if components.SETTINGS.get_debug_mode():
                            print(f"Неизвестный аргумент {command[1]} события {self.event_name}")
            # Изменение модуля Компьютер
            case "module_computer":
                # Второй аргумент
                match command[1]:
                    # Починить модуль
                    case "1":
                        components.GAME.player.module_computer_damaged = False
                    # Повредить модуль
                    case "0":
                        components.GAME.player.module_computer_damaged = True
                    case _:
                        if components.SETTINGS.get_debug_mode():
                            print(f"Неизвестный аргумент {command[1]} события {self.event_name}")
            # Изменение модуля Орудие
            case "module_weapon":
                # Второй аргумент
                match command[1]:
                    # Починить модуль
                    case "1":
                        components.GAME.player.module_weapon_damaged = False
                    # Повредить модуль
                    case "0":
                        components.GAME.player.module_weapon_damaged = True
                    case _:
                        if components.SETTINGS.get_debug_mode():
                            print(f"Неизвестный аргумент {command[1]} события {self.event_name}")
            case _:
                # Неизвестный аргумент.
                if components.SETTINGS.get_debug_mode():
                    print(
                        f"Аргумент события планеты {command[0]} в событии {self.event_name} не существует. Проверьте файл.")

    # Запуск события (или событий)
    def run_event(self) -> bool:
        if random.random() < self.event_prob / 4:
            # Не повезло в этот раз
            if components.SETTINGS.get_debug_mode():
                print(f"Ожидалось событие {self.event_name} на планете, но в этот раз не повезло.")
            return False
        if len(self.event_commands) < 1:
            if components.SETTINGS.get_debug_mode():
                print(f"События не найдены. Возможно, планета без событий.")
            return True

        for item in self.event_commands:
            c = item.split()
            # Вероятно, это неправильная команда
            if len(c) < 2:
                if components.SETTINGS.get_debug_mode():
                    print(f"Проверьте правильность события {self.event_name}. Вероятно, оно содержит ошибки.")
                continue
            # Выполняем команду
            self.handle_event_command(c)

        return True
