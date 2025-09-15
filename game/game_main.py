import datetime
import os.path

import keyboard as kb
from colorama import Fore, Back

from core.console_manager import clear_terminal, print_colored_text
from core.constants import DEBUG_MODE_ENABLED
from core.core_utils import pause
from core.menu_shared_functions import menu_unknown_key_code
from core.menus import main_menu
from game.classes.ship import PlayerShip
from game.classes.universe import Universe

UNIVERSE: Universe
PLAYER: PlayerShip

PAUSED = False

# Обработка ввода на экране паузы
def pause_input():
    key = kb.read_key()
    if DEBUG_MODE_ENABLED:
        print(key)
    global PAUSED
    match key:
        case "delete":
            # Останавливаем игру, пока что не реализовано
            clear_terminal()
            main_menu.run_main_menu()
        case "enter":
            # Продолжаем игру
            PAUSED = False
            clear_terminal(False)
            show_main_game_screen()
        case _:
            menu_unknown_key_code()

    if PAUSED:
        pause_input()

# Выводит экран паузы
def show_pause_screen():
    global PAUSED
    PAUSED = True
    # В будущем нужно реализовать паузу, сейчас её нет. Как и игры.
    text = "=== Пауза ===\nENTER - вернуться в игру\nDEL - выйти в главное меню"
    clear_terminal(False)
    if DEBUG_MODE_ENABLED:
        print("Остановка игры: пауза")
    print_colored_text(text)
    pause_input()

# Обработка команд в зависимости от действия
def game_commands(keycode: str):
    match keycode:
        case "esc":
            show_pause_screen()
        case _:
            menu_unknown_key_code()
    if not PAUSED:
        game_input()

# Ввод игры
def game_input():
    key = kb.read_key()
    game_commands(key)

# Возвращает дату в таком формате: день, месяц, год
def gui_launch_get_date() -> str:
    return f"{datetime.date.today().day}/{datetime.date.today().month}/{datetime.date.today().year}"

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
        f"Корабль {PLAYER.name}" + " " * 10,
        f"Уровень: {PLAYER.level}" + " " * 10,
        "======" + " " * 10,
        f"Прочность корабля: {PLAYER.health}%" + " " * 10,
        f"Уровень кислорода: {PLAYER.oxygen}%" + " " * 10,
        f"Скорость: {PLAYER.speed}" + " " * 10,
        "======" + " " * 10,
        f"Ресурсы: {PLAYER.resources}" + " " * 10,
    ]
    return l

def get_main_buttons_tip_text() -> str:
    text = (
        "\n\n[ESC] - Пауза | [M] - Карта | [R] - Ремонт"
    )
    return text


# Симуляция запуска компьютера
def animate_gui_launch():
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
    print_colored_text(f"> Последнее обновление прошивки: {gui_launch_get_date()}")
    pause(0.75)

    clear_terminal()
    print_colored_text("Оптимизация оболочки")
    for n in range(10):
        print_colored_text("[" + "=" * n + "]")
        pause(0.1)

    print_colored_text("Нет соединения с сервером, получение данных о планетах невозможно", Fore.YELLOW)
    pause(0.25)
    clear_terminal()
    show_main_game_screen()

# Показывает основной экран игры, где нарисован корабль и показано текущее состояние (здоровье, воздух и т.д.)
def show_main_game_screen():
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


# Запускает интерфейс игры
def run_game_gui():
    clear_terminal()
    animate_gui_launch()
    game_input()
