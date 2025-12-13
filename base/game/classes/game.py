import asyncio
import datetime
import random

import colorama
import playsound3

from base.core import components
from base.game.classes.planet import Planet
from base.game.classes.ship import Ship


# Выводит на экран текст помощи (основной)
def print_terminal_help():
    text = (
        f"{colorama.Fore.CYAN}Инструкция по использованию терминала.\n\n"
        f"{colorama.Fore.GREEN}Терминал - это проводник между Вами и Бортовым Компьютером. Введите команду, чтобы выполнить какое-то действие.\n"
        "Запущенный терминал автоматически приостанавливает игру, а Бортовой Компьютер ожидает Ваших команд.\n\n"
        "Ниже вы увидите общие команды терминала:\n"
        f"{colorama.Fore.CYAN}stop{colorama.Fore.GREEN} - Выход в главное меню игры без сохранения (не путать с терминалом)\n"
        f"{colorama.Fore.CYAN}help{colorama.Fore.GREEN} - Помощь с терминалом.\n"
        f"{colorama.Fore.CYAN}exit{colorama.Fore.GREEN} - Выход из терминала.\n"
        f"{colorama.Fore.CYAN}save{colorama.Fore.GREEN} - Сохранить игру.\n"
        "\n"
        "Чтобы открыть инструкции для других элементов игры, введите следующие команды:\n"
        f"{colorama.Fore.CYAN}help game{colorama.Fore.GREEN} - Как играть.\n"
        f"{colorama.Fore.CYAN}help ship{colorama.Fore.GREEN} - Инструкции по управлению кораблём.\n"
        f"{colorama.Fore.CYAN}help planets{colorama.Fore.GREEN} - Небольшая справка по планетам\n"
    )
    print(text)


# Выводит на экран текст помощи по игре
def print_game_help():
    text = (
        f"{colorama.Fore.CYAN}Как играть\n\n"
        f"{colorama.Fore.GREEN}2077 год. Вы - Капитан исследовательского космического корабля. Огромный астероид уничтожил всё живое на Земле.\n"
        f"Вы понимаете, что рано или поздно погибните. Ваша задача - продержаться как можно дольше\n\n"
        f"Исследуйте планеты, чтобы получать {colorama.Fore.CYAN}ресурсы{colorama.Fore.GREEN}. {colorama.Fore.CYAN}Ресурсы{colorama.Fore.GREEN} - это внутри-игровая валюта, при помощи которой Вы можете выполнять многие действия.\n"
        f"При помощи {colorama.Fore.CYAN}ресурсов{colorama.Fore.GREEN} Вы можете ремонтировать и улучшать корабль, создавать различные предметы (например, огнетушители) и т.д.\n\n"
        f"Во время игры Вы можете столкнуться с {colorama.Fore.CYAN}различными событиями{colorama.Fore.GREEN}, включая поломки на корабле или опасности на планетах. Будьте готовы к неприятностям!\n\n"
        f"{colorama.Fore.CYAN}Следите за характеристиками корабля{colorama.Fore.GREEN}. Если закончится топливо, Вы, вероятно, не сможете долететь до планеты, а значит {colorama.Fore.RED}игра закончится{colorama.Fore.GREEN}.\n"
        f"Вы проиграете, когда здоровье экипажа опустится до {colorama.Fore.RED}0{colorama.Fore.GREEN}. Ремонтируйте корабль и создавайте топливо, чтобы избежать этого.\n\n"
    )
    print(text)


# Выводит на экран текст помощи по управлению кораблём
def print_ship_help():
    text = (
        f"{colorama.Fore.CYAN}Инструкции по управлению кораблём\n\n"
        f"{colorama.Fore.GREEN}Основные команды:\n"
        f"{colorama.Fore.CYAN}rename [НАЗВАНИЕ]{colorama.Fore.GREEN} - Изменяет название корабля на [НАЗВАНИЕ]. Это бесплатно и ни на что не влияет.\n"
        f"{colorama.Fore.CYAN}status{colorama.Fore.GREEN} - Выводит информацию о статусе систем корабля.\n"
        f"{colorama.Fore.CYAN}goto [ID]{colorama.Fore.GREEN} - Отправиться на планету с выбранным ID\n"
        f"{colorama.Fore.CYAN}goto leave{colorama.Fore.GREEN} - Покинуть планету\n"
        f"{colorama.Fore.CYAN}goto cancel{colorama.Fore.GREEN} - Отменить полёт\n"
        f"{colorama.Fore.CYAN}repair [todo]{colorama.Fore.GREEN} - Начать ремонт корабля. Для 1 секунды ремонта требуется 5 ресурсов. todo"
    )
    print(text)


# Выводит на экран текст помощи по планетам
def print_planets_help(planets_count: int):
    text = (
        f"{colorama.Fore.CYAN}Справка по планетам\n\n"
        f"{colorama.Fore.GREEN}В процессе игры Вы можете исследовать различные планеты. Каждая планета по-своему уникальная, поэтому будьте осторожны.\nЧтобы Вам было интереснее играть, Мы не будем подробно описывать, что вас ждет на планетах, но познакомим с базовыми механиками игры.\n\n"
        f"{colorama.Fore.GREEN}Каждая планета имеет свой определенный тип и уровень опасности.\n"
        f"{colorama.Fore.CYAN}Уровень опасности{colorama.Fore.GREEN} - это показатель, который говорит о том, насколько {colorama.Fore.RED}враждебна{colorama.Fore.GREEN} планета для Вас.\n"
        f"{colorama.Fore.CYAN}Тип планеты{colorama.Fore.GREEN} - обозначает её состав, ландшафт, ресурсы, а также возможные опасности.\n"
        f"{colorama.Fore.GREEN}Самыми опасными планетами являются {colorama.Fore.CYAN}токсичные{colorama.Fore.GREEN}, но на них Вы сможете найти наибольшее количество ресурсов.\n\n"
        f"{colorama.Fore.GREEN}Приятного изучения космоса!\n\n"
        f"{colorama.Fore.GREEN}Основные команды:\n"
        f"{colorama.Fore.CYAN}planet [ЧИСЛО]{colorama.Fore.GREEN} - Информация о планете. При помощи {colorama.Fore.CYAN}[ЧИСЛО]{colorama.Fore.GREEN} вы можете указать номер планеты. {colorama.Fore.CYAN}[ЧИСЛО]{colorama.Fore.GREEN} должно находиться в пределах от 0 до {planets_count}. Если не указать, будет выбрана случайная планета.\n"
    )
    print(text)


# Возвращает новое значение в пределах от min_value до max_value
def clamp(value, min_value, max_value):
    if value > max_value:
        return max_value
    if value < min_value:
        return min_value
    return value


# Вычисляет время до завершения полёта, в секундах
def calculate_time(ship_speed: int, planet_distance: int) -> int:
    return planet_distance // ship_speed


# Возвращает обновленное значение скорости
def calculate_speed(ship: Ship) -> int:
    current_speed = ship.speed
    if ship.fuel < 1:
        # Если закончилось топливо
        if random.random() < 0.6:
            # Если повезло
            current_speed = clamp(current_speed - random.randint(10, 50), 0, 700)
    else:
        if (random.random() < 0.6 and current_speed < 549) or current_speed < 350:
            # Если повезло и скорость меньше 549 ИЛИ скорость меньше 350, то мы можем увеличить её
            current_speed = clamp(current_speed + random.randint(40, 150), 125, 700)
        else:
            # В другом случае уменьшаем, чтобы создать ощущение реального полёта
            current_speed = clamp(current_speed - random.randint(25, 50), 125, 700)
    # Без изменений
    return current_speed


# Возвращает обновленное значение топлива
def update_fuel(ship: Ship) -> int:
    # Если топливный бак пробит
    if ship.module_fuel_tank_damaged:
        if random.random() > 0.75:
            ship.fuel = clamp(ship.fuel - 1, 0, 100)

    if random.random() > 0.89:
        # Если повезло
        return clamp(ship.fuel - 1, 0, 100)
    else:
        # Без изменений
        return ship.fuel


# Возвращает обновленное значение кислорода
def update_oxygen(ship: Ship) -> int:
    # Если система жизнеобеспечения повреждена
    if ship.module_life_support_damaged and random.random() > 0.6:
        ship.oxygen = clamp(ship.oxygen - 1, 0, 100)

    if random.random() > 0.5 and ship.fuel < 1:
        # Если закончилось топливо и повезло
        return clamp(ship.oxygen - random.randint(1, 5), 0, 100)
    elif ship.strength < 1:
        # Если корабль разрушен
        return clamp(ship.oxygen - random.randint(1, 10), 0, 100)
    else:
        # Без изменений
        return ship.oxygen


# Возвращает цвет для переменных с процентами.
def get_percentage_value_color(m: int):
    if m > 50:
        return colorama.Fore.CYAN
    if 50 >= m >= 25:
        return colorama.Fore.YELLOW
    if m < 25:
        return colorama.Fore.RED

    return colorama.Fore.CYAN


# Класс игры
class Game:

    def __init__(self):
        self.paused = False  # Игра приостановлена?
        self.running = False  # Игра запущена?
        self.pending_update = False  # Ожидается ли обновление экрана?
        self.planet_flying_active = False  # Летит ли игрок на планету?
        self.player: Ship = Ship("")  # Корабль игрока. При создании используется пустышка.
        self.player_drawing: str = ''  # ASCII рисунок корабля
        self.planets: list[Planet] = []  # Список планет
        self.last_messages: list[str] = []  # Список последних действий
        self.timer = -1  # Простой таймер, который нужен для вывода времени ожидания какого-то действия. Если -1, значит он не работает
        self.audio_queue: list[str] = []  # Очередь звуков, здесь хранится путь до файлов

    # Генерирует текст информации о корабле в игре.
    # В чём суть:
    # Берём рисунок корабля, затем заменяем p на данные о корабле. Если осталось свободное место, заменяем p на пустоту.
    # Вместо s может нарисовать звёзды.
    def generate_main_text(self) -> str:
        # Если компьютер повреждён, есть шанс, что вместо информации о корабле будет написано ошибка.
        def get_ship_state_value_text(value) -> str:
            if self.player.module_computer_damaged and random.random() > 0.7:
                return f"{colorama.Fore.RED}ошибка "
            else:
                return value

        d = self.player_drawing.splitlines()

        computer_text = [
            f"Корабль " + f"{colorama.Fore.CYAN}{get_ship_state_value_text(self.player.ship_name)}" + colorama.Fore.GREEN,
            colorama.Fore.GREEN + "=" * 15,
        ]
        if self.player.on_planet:
            planet = self.get_planet_by_id(self.player.planet_id)
            computer_text += [
                colorama.Fore.GREEN + f"Сейчас мы находимся на планете " + colorama.Fore.CYAN + f"{get_ship_state_value_text(planet.planet_name)}" + colorama.Fore.GREEN,
                colorama.Fore.GREEN + "=" * 15,
            ]
        else:
            computer_text += [
                colorama.Fore.GREEN + f"Скорость: " + colorama.Fore.CYAN + f"{get_ship_state_value_text(self.player.speed)} км/с" + colorama.Fore.GREEN,
            ]

        computer_text += [
            colorama.Fore.GREEN + f"Температура внутри: {colorama.Fore.CYAN}{get_ship_state_value_text(self.player.inside_temperature)}°C" + colorama.Fore.GREEN,
            colorama.Fore.GREEN + f"Температура за бортом: {colorama.Fore.CYAN}{get_ship_state_value_text(self.player.outside_temperature)}°C" + colorama.Fore.GREEN,
            colorama.Fore.GREEN + f"Здоровье экипажа: " + get_percentage_value_color(
                self.player.crew_health) + f"{get_ship_state_value_text(self.player.crew_health)}%" + colorama.Fore.GREEN,
            colorama.Fore.GREEN + f"Прочность: " + get_percentage_value_color(
                self.player.strength) + f"{get_ship_state_value_text(self.player.strength)}%" + colorama.Fore.GREEN,
            colorama.Fore.GREEN + f"Ресурсы: " + colorama.Fore.CYAN + f"{get_ship_state_value_text(self.player.resources)}" + colorama.Fore.GREEN,
            colorama.Fore.GREEN + f"Кислород: " + get_percentage_value_color(
                self.player.oxygen) + f"{get_ship_state_value_text(self.player.oxygen)}%" + colorama.Fore.GREEN,
        ]
        if not self.player.on_planet:
            computer_text += [
                colorama.Fore.GREEN + f"Топливо: " + get_percentage_value_color(
                    self.player.fuel) + f"{get_ship_state_value_text(self.player.fuel)}%" + colorama.Fore.GREEN
            ]
        computer_text += [
            colorama.Fore.GREEN + "=" * 15,
            colorama.Fore.GREEN + f"Прожито дней: " + colorama.Fore.CYAN + f"{self.player.day}" + colorama.Fore.GREEN,
            colorama.Fore.GREEN + "=" * 15,
            colorama.Fore.GREEN + "ПОСЛЕДНИЕ ДЕЙСТВИЯ:"
        ]

        result = colorama.Fore.GREEN + ''
        c = 0
        wc = 0
        for line in d:
            # Если игрок на планете, нам не нужно рисовать звезды.
            if self.player.on_planet:
                line = line.replace("s", " ")
            else:
                n = 0
                text = list(line)
                for symbol in text:
                    if symbol == "s":
                        if random.random() > 0.9:
                            text[n] = f"{colorama.Fore.WHITE}*{colorama.Fore.GREEN}"
                        else:
                            text[n] = " "
                    n += 1
                line = ''.join(text)
                del text
                del n

            if c < len(computer_text):
                result += f"\n{line.replace("p", computer_text[c])}"
            else:
                if wc < len(self.last_messages):
                    result += f"\n{line.replace("p", self.last_messages[wc])}"
                    wc += 1
                else:
                    result += f"\n{line.replace("p", "")}"
                    if len(d) - 1 == c:
                        result += f"\n{line.replace("p", "\n")}"
                        result += "Для запуска терминала нажмите <ПРОБЕЛ>\nЕсли возникнут трудности, введите команду help."

            c += 1

        return result

    # Возвращает текст со статусом систем корабля
    def get_ship_status_text(self) -> str:

        def get_module_status_text(value: bool) -> str:
            return f'{colorama.Fore.RED}повреждено' if value else f'{colorama.Fore.GREEN}работает'

        result = (
            f"{colorama.Fore.GREEN}Основные системы:\n"
            f"{colorama.Fore.CYAN}Системы жизнеобеспечения: {get_module_status_text(self.player.module_life_support_damaged)}\n"
            f"{colorama.Fore.CYAN}Система охлаждения двигателей: {get_module_status_text(self.player.module_cooling_system_damaged)}\n"
            f"{colorama.Fore.CYAN}Бортовой компьютер: {get_module_status_text(self.player.module_computer_damaged)}\n"
            f"{colorama.Fore.GREEN}Корабль:\n"
            f"{colorama.Fore.CYAN}Двигатель: {get_module_status_text(self.player.module_main_engine_damaged)}\n"
            f"{colorama.Fore.CYAN}Топливный бак: {get_module_status_text(self.player.module_fuel_tank_damaged)}\n"
            f"{colorama.Fore.CYAN}Орудие: {get_module_status_text(self.player.module_weapon_damaged)}\n"
        )
        return result

    # Возвращает планету по её ID
    def get_planet_by_id(self, m_id: int) -> Planet:
        if self.planets is None:
            if components.SETTINGS.get_debug_mode():
                print(colorama.Fore.RED + "Список планет не был загружен.")
            return Planet(0, "None", "None", 0, 0, 0, 0)

        l = [x for x in self.planets if x.planet_id == m_id]
        if len(l) < 1:
            if components.SETTINGS.get_debug_mode():
                print(colorama.Fore.YELLOW + "Планета не обнаружена, возвращаем случайную")
            return random.choice(self.planets)
        pl = l[0]
        del l
        return pl

    # Возвращает текст описания планеты
    def get_text_planet_list(self, position: int) -> str:

        if self.planets is None:
            return f'{colorama.Fore.RED}Внутренняя ошибка ядра системы. Невозможно получить описание планет.'

        # Возвращает цвет текста для уровня опасности планеты
        def get_danger_color(value: int):
            if value >= 7:
                return colorama.Fore.RED
            elif 7 > value > 3:
                return colorama.Fore.YELLOW
            elif value < 4:
                return colorama.Fore.GREEN
            else:
                return colorama.Fore.CYAN

        if position < 0 or position > len(self.planets) - 1:
            return f'{colorama.Fore.RED}Укажите число в диапазоне от {colorama.Fore.CYAN}0{colorama.Fore.RED} до {colorama.Fore.CYAN}{len(self.planets) - 1}{colorama.Fore.RED}'
        planet: Planet = self.planets[position]
        text = (
            f"{colorama.Fore.GREEN}Планета: {colorama.Fore.CYAN}{planet.planet_name}{colorama.Fore.GREEN}\n"
            f"{colorama.Fore.GREEN}ID: {colorama.Fore.CYAN}{planet.planet_id}{colorama.Fore.GREEN}\n\n"
            f"{colorama.Fore.GREEN}Описание: {planet.planet_description}\n\n"
            f"{colorama.Fore.GREEN}Тип планеты: {colorama.Fore.CYAN}{planet.get_planet_type_name()}{colorama.Fore.GREEN}\n"
            f"{get_danger_color(planet.planet_danger)}Средняя температура: {planet.planet_temp}°C{colorama.Fore.GREEN}\n"
            f"{get_danger_color(planet.planet_danger)}Уровень опасности: {planet.planet_danger}{colorama.Fore.GREEN}\n\n"
        )
        del planet
        return text

    # Добавляет событие в список
    def update_last_messages(self, new_message: str):
        self.last_messages = [f"{datetime.datetime.now().strftime("%H:%M:%S")} : {new_message}{colorama.Fore.GREEN}"] + self.last_messages
        # Если количество элементов превышает лимит, ликвидируем самое старое
        if len(self.last_messages) > 12:
            self.last_messages.pop()

    # Создаёт случайные события в игре
    async def events_generator(self):
        if self.player.on_planet:
            # События, которые происходят только на планетах
            pass
        else:
            # События, которые происходят только в космосе
            # todo: нужно наконец начать делать события
            pass

    # Добавляет путь к файлу со звуком в очередь.
    def add_audio_to_queue(self, path: str) -> bool:
        # Нет смысла использовать очередь звуков, если звуки отключены.
        if not components.SETTINGS.sound:
            return False
        self.audio_queue.append(path)
        return True

    # Проигрывает звуки в очереди.
    async def audio_loop(self):
        # Нет смысла запускать этот цикл, если звуки отключены
        if not components.SETTINGS.sound:
            return
        while components.ENGINE.running:
            # Если движок был остановлен, то нужно остановить
            if not components.ENGINE.running:
                break
            if len(self.audio_queue) < 1:
                await asyncio.sleep(0.1)
                continue
            path = self.audio_queue[0]
            if components.SETTINGS.debug_mode:
                print(f"Путь до звука: {path}")
            sound = playsound3.playsound(path, False)
            # Ждём, когда звук закончится
            while sound.is_alive():
                await asyncio.sleep(0.1)
            # Избавляемся от него
            del path
            self.audio_queue.pop(0)

    # Основной цикл игры
    async def main_loop(self):
        # Здесь хранятся переменные, контролирующие уведомления
        low_fuel_notification_enabled = True
        no_fuel_notification_enabled = True
        low_strength_notification_enabled = True
        no_strength_notification_enabled = True
        low_oxygen_notification_enabled = True
        no_oxygen_notification_enabled = True
        temperature_notification_enabled = True

        # Уведомления для модулей
        module_main_engine_notification_enabled = True
        module_fuel_tank_notification_enabled = True
        module_cooling_system_notification_enabled = True
        module_life_support_notification_enabled = True
        module_computer_notification_enabled = True
        module_weapon_notification_enabled = True

        all_modules_damaged_notification_enabled = True

        # Обновляет температуру
        def update_temperature():
            if self.player.on_planet:
                pl = self.get_planet_by_id(self.player.planet_id)

                # Если температура на планете выше 100 C
                if pl.planet_temp > 100:
                    if pl.planet_type in [3, 5]:
                        self.player.inside_temperature = clamp(self.player.inside_temperature + random.randint(-1,
                                                                                                               8 if not self.player.module_life_support_damaged else 14),
                                                               0,
                                                               55 if not self.player.module_life_support_damaged else 90)
                    else:
                        self.player.inside_temperature = clamp(self.player.inside_temperature + random.randint(-1,
                                                                                                               4 if not self.player.module_life_support_damaged else 8),
                                                               0,
                                                               35 if not self.player.module_life_support_damaged else 55)
                # Если температура на планете ниже -100 C
                elif pl.planet_temp < -100:
                    if pl.planet_type in [1, 2, 4]:
                        self.player.inside_temperature = clamp(self.player.inside_temperature + random.randint(
                            -4 if not self.player.module_life_support_damaged else -8, 1),
                                                               -50 if not self.player.module_life_support_damaged else -90,
                                                               20)
                    else:
                        self.player.inside_temperature = clamp(self.player.inside_temperature + random.randint(
                            -2 if not self.player.module_life_support_damaged else -1, 1),
                                                               -45 if not self.player.module_life_support_damaged else -65,
                                                               20)

                self.player.outside_temperature = clamp(pl.planet_temp + random.randint(-2, 2), pl.planet_temp - 15,
                                                        pl.planet_temp + 15)
                del pl
            else:
                min_inside_temp = 17 if not self.player.module_life_support_damaged else -30
                max_inside_temp = 25 if not self.player.module_life_support_damaged else 45

                if self.player.inside_temperature < min_inside_temp:
                    self.player.inside_temperature += 2 if not self.player.module_life_support_damaged else 1
                elif self.player.inside_temperature > max_inside_temp:
                    self.player.inside_temperature -= 2 if not self.player.module_life_support_damaged else 1
                else:
                    self.player.inside_temperature = clamp(self.player.inside_temperature + random.randint(
                        -1 if not self.player.module_life_support_damaged else -4,
                        1 if not self.player.module_life_support_damaged else 4),
                                                           min_inside_temp, max_inside_temp)

                self.player.outside_temperature = clamp(self.player.outside_temperature + random.randint(-2, 2),
                                                        -273,
                                                        -180)

        c = 0  # Простой счетчик, который нужен для обновления количества дней.
        while components.ENGINE.running:
            # Если движок был остановлен, то нужно остановить игру
            if not components.ENGINE.running and not self.running:
                break
            # Если игрок еще не был загружен или игра приостановлена (например, ожидается ввод игрока), пропускаем итерацию, засыпая на секунду.
            if self.player.ship_name == "" or self.paused or components.ENGINE.pending_input:
                await asyncio.sleep(1)
                continue

            # Если экипаж погибает, игра завершается. Увы.
            if self.player.crew_health < 1:
                if components.SETTINGS.get_debug_mode():
                    print("Игра закончилась, игрок погиб.")
                print(
                    f"{colorama.Fore.BLACK}{colorama.Back.RED}ИГРА ЗАВЕРШЕНА: ВЫ ПОГИБЛИ{colorama.Back.RESET}{colorama.Fore.GREEN}")
                for _ in range(3):
                    self.update_last_messages(
                        f"{colorama.Fore.BLACK}{colorama.Back.RED}ИГРА ЗАВЕРШЕНА: ВЫ ПОГИБЛИ{colorama.Back.RESET}{colorama.Fore.GREEN}")
                self.update_last_messages(
                    f"{colorama.Fore.BLACK}{colorama.Back.RED}Используйте команду stop, чтобы выйти в главное меню.{colorama.Back.RESET}{colorama.Fore.GREEN}")
                self.pending_update = True
                self.running = False
                components.ENGINE.blocked = True
                await asyncio.sleep(5)
                components.ENGINE.blocked = False
                if components.SETTINGS.get_debug_mode():
                    print("Игра была завершена")
                # Костыль, чтобы цикл никогда не завершался.
                self.player.ship_name = ""
                continue

            # Обновляет температуру
            update_temperature()

            # Если игрок не на планете, изменяем скорость и топливо
            if not self.player.on_planet:
                self.player.speed = calculate_speed(self.player)
                self.player.fuel = update_fuel(self.player)

            self.player.oxygen = update_oxygen(self.player)

            # ТЕМПЕРАТУРА
            if self.player.inside_temperature > 39:
                if random.random() > 0.6:
                    self.player.crew_health = clamp(self.player.crew_health - 1, 0, 100)
                if temperature_notification_enabled:
                    temperature_notification_enabled = False
                    self.update_last_messages(f"{colorama.Fore.RED}Крайне высокая температура внутри корабля!")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//very_high_temp_warning.mp3")
            elif self.player.inside_temperature < -24:
                if random.random() > 0.6:
                    self.player.crew_health = clamp(self.player.crew_health - 1, 0, 100)
                if temperature_notification_enabled:
                    temperature_notification_enabled = False
                    self.update_last_messages(f"{colorama.Fore.RED}Крайне низкая температура внутри корабля!")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//very_low_temp_warning.mp3")
            else:
                if not temperature_notification_enabled:
                    temperature_notification_enabled = True
            # ТЕМПЕРАТУРА КОНЕЦ

            # ТОПЛИВО
            if self.player.fuel > 10:
                if not low_fuel_notification_enabled:
                    low_fuel_notification_enabled = True
            if 1 < self.player.fuel < 10:
                if low_fuel_notification_enabled:
                    low_fuel_notification_enabled = False
                    self.update_last_messages(f"{colorama.Fore.YELLOW}Низкий уровень топлива!")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//low_fuel_warning.mp3")
            if self.player.fuel < 1:
                if no_fuel_notification_enabled:
                    no_fuel_notification_enabled = False
                    self.update_last_messages(
                        f"{colorama.Fore.BLACK}{colorama.Back.RED}Закончилось топливо!{colorama.Back.RESET}{colorama.Fore.GREEN}")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//no_fuel_warning.mp3")
            if self.player.fuel > 1:
                if not no_fuel_notification_enabled:
                    no_fuel_notification_enabled = True
            # ТОПЛИВО - КОНЕЦ

            # ПРОЧНОСТЬ
            if self.player.strength > 25:
                if not low_strength_notification_enabled:
                    low_strength_notification_enabled = True
            if 1 < self.player.strength < 25:
                if low_strength_notification_enabled:
                    low_strength_notification_enabled = False
                    self.update_last_messages(f"{colorama.Fore.YELLOW}Корпус критически повреждён!")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//low_strength_warning.mp3")
            if self.player.strength < 1:
                if no_strength_notification_enabled:
                    no_strength_notification_enabled = False
                    self.update_last_messages(
                        f"{colorama.Fore.BLACK}{colorama.Back.RED}Корпус разрушен!{colorama.Back.RESET}{colorama.Fore.GREEN}")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//no_strength_warning.mp3")
            if self.player.strength > 1:
                if not no_strength_notification_enabled:
                    no_strength_notification_enabled = True
            # ПРОЧНОСТЬ - КОНЕЦ

            # КИСЛОРОД
            if self.player.oxygen > 20:
                if not low_oxygen_notification_enabled:
                    low_oxygen_notification_enabled = True
            if 1 < self.player.oxygen < 20:
                if low_oxygen_notification_enabled:
                    low_oxygen_notification_enabled = False
                    self.update_last_messages(f"{colorama.Fore.YELLOW}Критически низкий уровень кислорода!")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//low_oxygen_warning.mp3")
            if self.player.oxygen < 1:
                # Если кислород на нуле, наносим урон экипажу с шансом 70%
                if random.random() > 0.3:
                    self.player.crew_health = clamp(self.player.crew_health - random.randint(1, 4), 0, 100)
                if no_oxygen_notification_enabled:
                    no_oxygen_notification_enabled = False
                    self.update_last_messages(
                        f"{colorama.Fore.BLACK}{colorama.Back.RED}Кислород закончился!{colorama.Back.RESET}{colorama.Fore.GREEN}")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//no_oxygen_warning.mp3")
            if self.player.oxygen > 1:
                if not no_oxygen_notification_enabled:
                    no_oxygen_notification_enabled = True
            # КИСЛОРОД - КОНЕЦ

            # Проверка модулей корабля
            # Двигатель
            if self.player.module_main_engine_damaged:
                if module_main_engine_notification_enabled:
                    module_main_engine_notification_enabled = False
                    self.update_last_messages(f"{colorama.Fore.RED}Двигатель повреждён, максимальная скорость снижена!")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//engine_damaged.mp3")
            else:
                if not module_main_engine_notification_enabled:
                    module_main_engine_notification_enabled = True
                    self.update_last_messages(f"{colorama.Fore.GREEN}Двигатель восстановлен, можно лететь!")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//engine_repaired.mp3")

            # Топливный бак
            if self.player.module_fuel_tank_damaged:
                if module_fuel_tank_notification_enabled:
                    module_fuel_tank_notification_enabled = False
                    self.update_last_messages(f"{colorama.Fore.RED}Топливный бак повреждён!")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//fuel_tank_damaged.mp3")
            else:
                if not module_fuel_tank_notification_enabled:
                    module_fuel_tank_notification_enabled = True
                    self.update_last_messages(f"{colorama.Fore.GREEN}Топливный бак восстановлен!")
                    if components.SETTINGS.get_sound():
                        self.add_audio_to_queue("base//game//res//audio//fuel_tank_repaired.mp3")

            # Система охлаждения
            if self.player.module_cooling_system_damaged:
                if module_cooling_system_notification_enabled:
                    module_cooling_system_notification_enabled = False
                    self.update_last_messages(
                        f"{colorama.Fore.RED}Система охлаждения двигателей повреждена! Шанс пожара увеличен, максимальная скорость снижена.")
            else:
                if not module_cooling_system_notification_enabled:
                    module_cooling_system_notification_enabled = True
                    self.update_last_messages(f"{colorama.Fore.GREEN}Система охлаждения двигателей восстановлена.")

            # Система жизнеобеспечения
            if self.player.module_life_support_damaged:
                if module_life_support_notification_enabled:
                    module_life_support_notification_enabled = False
                    self.update_last_messages(
                        f"{colorama.Fore.RED}Система жизнеобеспечения повреждена! Стабилизация температуры недоступна, отключение подачи кислорода.")
            else:
                if not module_life_support_notification_enabled:
                    module_life_support_notification_enabled = True
                    self.update_last_messages(f"{colorama.Fore.GREEN}Система жизнеобеспечения восстановлена.")

            # Компьютер
            if self.player.module_computer_damaged:
                if module_computer_notification_enabled:
                    module_computer_notification_enabled = False
                    self.update_last_messages(
                        f"{colorama.Fore.RED}Бортовой компьютер повреждён! Сбой систем навигаций, нарушение работы терминала.")
            else:
                if not module_computer_notification_enabled:
                    module_computer_notification_enabled = True
                    self.update_last_messages(f"{colorama.Fore.GREEN}Бортовой компьютер восстановлен.")
            # todo: стрельба не реализована.
            # Орудие
            if self.player.module_weapon_damaged:
                if module_weapon_notification_enabled:
                    module_weapon_notification_enabled = False
                    self.update_last_messages(f"{colorama.Fore.RED}Орудие повреждено! Точность стрельбы снижена.")
            else:
                if not module_weapon_notification_enabled:
                    module_weapon_notification_enabled = True
                    self.update_last_messages(f"{colorama.Fore.GREEN}Орудие восстановлено.")
            # Уведомление о том, что повреждены все системы
            if self.player.are_all_system_damaged():
                if all_modules_damaged_notification_enabled:
                    all_modules_damaged_notification_enabled = False
                    self.update_last_messages(f"{colorama.Fore.RED}Внимание! Повреждение всех систем.")
                    self.add_audio_to_queue("base//game//res//audio//all_systems_damaged_warning.mp3")
            else:
                if not all_modules_damaged_notification_enabled:
                    all_modules_damaged_notification_enabled = True

            # Генерируем случайное событие, если повезет
            if random.random() > 0.9:
                await self.events_generator()

            # Обновление счётчика дней.
            c += 1
            if c > 60:
                self.player.day += 1
                c = 0

            # Помечаем, что ожидается обновление экрана.
            self.pending_update = True
            await asyncio.sleep(3)

    # Ремонт корабля, нужно доработать это.
    async def repair_cycle(self):
        repair_time = round(40 * (self.player.strength / 100))
        self.update_last_messages(
            f"{colorama.Fore.CYAN}Начинаем ремонт корабля!{colorama.Fore.GREEN}")
        while repair_time > 0:
            # Если движок был остановлен, то нужно остановить цикл
            if not components.ENGINE.running and not self.running:
                break
            # Если игра приостановлена, пропускаем итерацию
            if self.paused or components.ENGINE.pending_input:
                await asyncio.sleep(1)
                continue

            if repair_time % 3 == 0:
                self.update_last_messages(
                    f"{colorama.Fore.GREEN}Идёт ремонт корабля. Осталось: {colorama.Fore.CYAN}{repair_time}{colorama.Fore.GREEN} секунд.")
            repair_time -= 1
            await asyncio.sleep(1)
        # Если движок был остановлен, мы не можем продолжить ремонт
        if not components.ENGINE.running:
            return

        # Ремонт завершён
        del repair_time
        self.timer = -1
        self.update_last_messages(f"{colorama.Fore.GREEN}Ремонт успешно завершён!")

    # Цикл полёта.
    async def fly_cycle(self, time: int, leave_planet: bool):
        self.planet_flying_active = True

        final_time = random.randint(time - 20, time + 40) if not leave_planet else random.randint(20, 40)
        # Увеличиваем время полёта, если двигатель повреждён.
        if self.player.module_main_engine_damaged:
            final_time += random.randint(10, 40)
        # Немного увеличиваем время полёта, если система охлаждения повреждена.
        if self.player.module_cooling_system_damaged:
            final_time += random.randint(5, 25)
        # В режиме отладки время полёта значительно меньше
        if components.SETTINGS.get_debug_mode():
            final_time = 8

        planet = self.get_planet_by_id(self.player.planet_id)

        successful = True

        # Повреждает все модули на корабле с шансом 50% на каждый
        def damage_all_modules():
            if random.random() > 0.5:
                self.player.module_main_engine_damaged = True
            if random.random() > 0.5:
                self.player.module_fuel_tank_damaged = True
            if random.random() > 0.5:
                self.player.module_cooling_system_damaged = True
            if random.random() > 0.5:
                self.player.module_life_support_damaged = True
            if random.random() > 0.5:
                self.player.module_computer_damaged = True
            if random.random() > 0.5:
                self.player.module_weapon_damaged = True

        while final_time > 0:

            # Если движок был остановлен ИЛИ полёт был отменен, то нужно остановить цикл
            if not components.ENGINE.running and not self.running:
                successful = False
                break

            # Если полёт был отменен, то нужно остановить цикл.
            if not self.planet_flying_active:
                self.update_last_messages(f"{colorama.Fore.RED}Полёт был отменён.")
                successful = False
                break
            # Если игра приостановлена, пропускаем итерацию
            if self.paused or components.ENGINE.pending_input:
                await asyncio.sleep(1)
                continue

            # Завершаем полет, если топливо закончилось
            if self.player.fuel < 1:
                successful = False
                if final_time < 5 and leave_planet:
                    self.update_last_messages(
                        f"{colorama.Fore.YELLOW}Мы покинули планету {planet.planet_name}, но двигатели заглохли. Причина: {colorama.Fore.RED}Недостаточно топлива.")
                    components.GAME.player.planet_id = -1
                    components.GAME.player.on_planet = False
                elif final_time < 5 and not leave_planet:
                    self.update_last_messages(
                        f"{colorama.Fore.YELLOW}Жёсткая посадка! Причина: {colorama.Fore.RED}Недостаточно топлива для завершения полёта")
                    components.GAME.player.planet_id = self.player.planet_id
                    components.GAME.player.on_planet = True
                    damage_all_modules()
                else:
                    self.update_last_messages(
                        f"{colorama.Fore.RED}Двигатели заглохли, закончилось топливо. Невозможно продолжить полёт." if not leave_planet else f"{colorama.Fore.RED}Двигатели заглохли, закончилось топливо. Мы не смогли покинуть планету.")
                break

            if final_time % 10 == 0:
                self.update_last_messages(
                    f"{colorama.Fore.GREEN}Летим на планету {planet.planet_name}. Оставшееся время: {final_time} с" if not leave_planet else f"{colorama.Fore.GREEN}Покидаем планету {planet.planet_name}. Оставшееся время: {final_time} с")

            final_time -= 1
            await asyncio.sleep(1)

        # Если полёт не успешный, то прерываем работу функции.
        if not successful:
            del planet
            del final_time
            self.planet_flying_active = False
            return

        if leave_planet:
            self.update_last_messages(
                f"{colorama.Fore.BLACK}{colorama.Back.GREEN}Мы покинули планету {planet.planet_name}!{colorama.Back.RESET}")
            components.GAME.player.planet_id = -1
            components.GAME.player.on_planet = False
        else:
            self.update_last_messages(f"{colorama.Fore.GREEN}Добро пожаловать на планету {planet.planet_name}!")
            components.GAME.player.planet_id = self.player.planet_id
            components.GAME.player.on_planet = True

        del planet
        del final_time
        self.planet_flying_active = False
