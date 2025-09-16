import asyncio
import os.path

import keyboard as kb
from colorama import Fore, Back

from core.console_manager import clear_terminal, print_colored_text
from core.constants import DEBUG_MODE_ENABLED
from core.core_utils import pause
from core.menus import main_menu
from core.translation_manager import TRANSLATIONS
from game import game_threads
from game import game_vars
from game.game_utils import is_repair_needed, get_today_date


# Запускает основной поток игры
async def start_main_thread():
    if not game_vars.MAIN_GAME_THREAD_RUNNING:
        if DEBUG_MODE_ENABLED:
            print("Попытка запуска основного потока игры")
        game_vars.MAIN_GAME_THREAD_RUNNING = True  # Указываем, что поток запущен.
        asyncio.create_task(game_threads.main_thread())  # Запускаем


# Выводит экран паузы
def show_pause_screen():
    game_vars.PAUSED = True  # Указываем, что игра приостановлена.
    # В будущем нужно реализовать паузу, сейчас её нет. Как и игры.
    text = "=== Пауза ===\nENTER - вернуться в игру\nDEL - выйти в главное меню"
    clear_terminal(False)
    if DEBUG_MODE_ENABLED:
        print("Остановка игры: пауза")
    print_colored_text(text)


# Возвращает ASCII рисунок корабля
def get_player_ship_ascii(level: int) -> str:
    file = os.path.join("models", f"ship_v{level}.txt")
    if DEBUG_MODE_ENABLED:
        print(f"Загрузка рисунка корабля по пути {file}")
    if os.path.exists(file):
        result = ""
        with open(file) as f:
            for line in f:
                result += line
            return result
    else:
        print_colored_text("Критическая ошибка, рисунок корабля не найден. Продолжение игры невозможно.", Back.RED)
        exit(1)


# Возвращает информацию о корабле
def get_player_stats_list() -> list:
    l = [
        f"Корабль {game_vars.PLAYER.name}" + " " * 10,
        f"Уровень: {game_vars.PLAYER.level}" + " " * 10,
        "======" + " " * 10,
        f"Прочность корабля: {game_vars.PLAYER.health}%" + " " * 10,
        f"Топливо: {game_vars.PLAYER.fuel}%" + " " * 10,
        f"Кислород: {game_vars.PLAYER.oxygen}%" + " " * 10,
        f"Скорость: {game_vars.PLAYER.speed}" + " " * 10,
        "======" + " " * 10,
        f"Ресурсы: {game_vars.PLAYER.resources}" + " " * 10,
    ]
    return l


def get_main_buttons_tip_text() -> str:
    text = (
        "\n\n[ESC] - Пауза | [M] - Карта | [R] - Ремонт | [H] - Как играть?"
    )
    return text


# Симуляция запуска компьютера
def animate_gui_launch():
    # Если включен режим отладки, пропускаем бесполезные вещи.
    if not DEBUG_MODE_ENABLED:
        print_colored_text("> Проверка целостности системы: Успешно")
        print_colored_text("> Инициализация базовых систем")
        pause(1)
        print_colored_text("> Подготовка орудий ...")
        pause(0.75)
        print_colored_text("> Запуск оболочки SPACE_TERMINAL v.1.0 .")
        pause(0.75)
        print_colored_text("> Запуск оболочки SPACE_TERMINAL v.1.0 . .")
        pause(0.75)
        print_colored_text("> Запуск оболочки SPACE_TERMINAL v.1.0 . . .")
        print_colored_text("> Проверка безопасности системы : Ошибка", Fore.RED)
        print_colored_text("> Проверка связи: Успешно")
        pause(0.75)
        print_colored_text(f"> Последнее обновление прошивки: {get_today_date()}")
        pause(0.75)

        clear_terminal()
        print_colored_text("Оптимизация оболочки")
        for n in range(10):
            print_colored_text("[" + "=" * n + "]")
            pause(0.1)

        print_colored_text("Нет соединения с сервером, получение данных о планетах невозможно", Fore.YELLOW)
        pause(0.25)
    show_main_game_screen()


# Показывает основной экран игры, где нарисован корабль и показано текущее состояние (здоровье, воздух и т.д.)
def show_main_game_screen():
    clear_terminal(False)
    ship = get_player_ship_ascii(0)
    stats = get_player_stats_list()
    n = 0
    for s in ship:
        # Замена p на информацию о корабле. Если список данных заканчивается, p заменяются на пустоту.
        if s == "p":
            if n < len(stats):
                ship = ship.replace("p", stats[n], 1)
            else:
                ship = ship.replace("p", "")
            n = n + 1

    print_colored_text(ship + get_main_buttons_tip_text())


# Запускает функцию ремонта, если все условия выполнены.
async def run_repair():
    if DEBUG_MODE_ENABLED:
        print("Попытка начать ремонт")
    if is_repair_needed():
        if game_vars.PLAYER.resources > 10:
            asyncio.create_task(game_threads.repair())
        else:
            print_colored_text(Fore.BLACK + TRANSLATIONS['not_enough_resources'] + Back.RESET + Fore.RESET, Back.RED)
    else:
        print_colored_text(Fore.BLACK + TRANSLATIONS['repair_not_needed'] + Back.RESET + Fore.RESET, Back.YELLOW)

async def game_cycle():
    await start_main_thread()
    while True:
        if not game_vars.PAUSED:
            match game_vars.GAME_SCREEN:
                case "main":
                    if game_vars.UPDATE_REQUIRED:
                        game_vars.UPDATE_REQUIRED = False
                        show_main_game_screen()
                    if kb.is_pressed("r"):
                        await run_repair()

                case _:
                    pass

            if kb.is_pressed("esc"):
                show_pause_screen()
        else:
            if kb.is_pressed("delete"):
                # Останавливаем игру, пока что не реализовано
                clear_terminal()
                main_menu.run_main_menu()
            if kb.is_pressed("enter"):
                # Продолжаем игру
                game_vars.PAUSED = False
                show_main_game_screen()
                await start_main_thread()

        await asyncio.sleep(0.033)


# Запускает интерфейс игры
def run_game_gui():
    clear_terminal()
    animate_gui_launch()
    asyncio.run(game_cycle())
