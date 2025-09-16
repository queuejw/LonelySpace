import asyncio
import random

from core.constants import SHIP_LVL_0_SPEED, SHIP_LVL_1_SPEED, DEBUG_MODE_ENABLED, SHIP_LVL_2_SPEED, SHIP_LVL_3_SPEED
from core.core_utils import clamp
from game import game_vars
from game.classes.ship import PlayerShip

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


def calculate_new_speed(old, new) -> int:
    return (old + new) // 2


def update_ship_data(ship: PlayerShip) -> PlayerShip:
    ship.speed = clamp(calculate_new_speed(ship.speed, random.randint(ship.speed // 2, ship.speed * 2)), 0,
                       get_ship_max_speed(ship.level))
    return ship


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
            "Основной поток завершён, поскольку MAIN_GAME_THREAD_RUNNING == False. Возможно, игра завершилась, или была приостановлена?")
