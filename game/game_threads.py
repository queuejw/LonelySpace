import asyncio
import random

from colorama import Fore

from core.console_manager import print_colored_text
from core.constants import SHIP_LVL_0_SPEED, SHIP_LVL_1_SPEED, DEBUG_MODE_ENABLED, SHIP_LVL_2_SPEED, SHIP_LVL_3_SPEED
from core.core_utils import clamp
from core.translation_manager import TRANSLATIONS
from game import game_vars
from game.classes.ship import PlayerShip
from game.game_utils import is_repair_needed

main_n = 0  # Используется для вычисления количества циклов во время отладки.


# Возвращает максимальную скорость корабля
def get_ship_max_speed(lvl: int) -> int:
    match lvl:
        case 1:
            return SHIP_LVL_1_SPEED
        case 2:
            return SHIP_LVL_2_SPEED
        case 3:
            return SHIP_LVL_3_SPEED
        case _:
            return SHIP_LVL_0_SPEED


# Вычисляет среднюю скорость
def calculate_new_speed(old, new) -> int:
    return (old + new) // 2


# Возвращает корабль с обновленными значениями
def update_ship_data(ship: PlayerShip) -> PlayerShip:
    ship.speed = clamp(calculate_new_speed(ship.speed, random.randint(ship.speed // 2, ship.speed * 2)), 0,
                       get_ship_max_speed(ship.level))
    return ship


# Основной поток игры, в котором происходит вся "магия".
async def main_thread():
    if DEBUG_MODE_ENABLED:
        print("Основной поток запущен")

    while game_vars.MAIN_GAME_THREAD_RUNNING:

        if game_vars.PAUSED:
            # Если игра приостановлена, останавливаем основной поток игры.
            if DEBUG_MODE_ENABLED:
                print("Поток остановлен по причине паузы игры.")

            game_vars.MAIN_GAME_THREAD_RUNNING = False  # Указываем, что основной поток игры остановлен.
            return

        if DEBUG_MODE_ENABLED:
            global main_n
            main_n = main_n + 1
            print(f"{main_n} цикл основного потока")

        # Обновляем данные
        game_vars.PLAYER = update_ship_data(game_vars.PLAYER)
        game_vars.UPDATE_REQUIRED = True

        await asyncio.sleep(5)  # Ожидаем N секунд перед началом нового цикла.

    if DEBUG_MODE_ENABLED:
        print(
            "Основной поток завершён. Возможно, игра завершилась, или была приостановлена?")


# Ремонт корабля.
# Стоит учитывать, что ремонт будет работать даже во время паузы. Это не баг, это фича (мне лень реализовывать остановку цикла)
async def repair():
    game_vars.REPAIR_RUNNING = True  # Указываем, что ремонт идёт
    # Запускаем цикл со случайной длительностью (от 10 до 30 секунд)
    dur = random.randint(5, 30)
    if DEBUG_MODE_ENABLED:
        print(f"Начинается ремонт корабля длительностью {dur} секунд")
    for x in range(dur):

        if not is_repair_needed():
            break

        if game_vars.PLAYER.resources < 10:
            print_colored_text(TRANSLATIONS['not_enough_resources'], Fore.RED)
            break

        if game_vars.PLAYER.health < 100:
            game_vars.PLAYER.health = clamp(game_vars.PLAYER.health + random.randint(1, 2), 0, 100)

        if game_vars.PLAYER.oxygen < 100:
            game_vars.PLAYER.oxygen = clamp(game_vars.PLAYER.oxygen + random.randint(1, 2), 0, 100)

        await asyncio.sleep(1)  # Ожидаем 1 секунду перед следующей итерацией

    game_vars.REPAIR_RUNNING = False  # Указываем, что ремонт закончился.

    if game_vars.PLAYER.resources > 10:
        print_colored_text(TRANSLATIONS['repair_finished'])
