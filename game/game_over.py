import random

import keyboard
from colorama import Fore, Back

from core.console_manager import clear_terminal, print_colored_text
from core.core_utils import pause
from core.menus import main_menu
from game import game_vars


def clear_old_game_data():
    del game_vars.PLAYER
    del game_vars.UNIVERSE
    game_vars.MAIN_GAME_THREAD_RUNNING = False
    game_vars.UPDATE_REQUIRED = False
    game_vars.PAUSED = False
    game_vars.REPAIR_RUNNING = False


def print_random_system_error_text():
    if random.random() > 0.5:
        print_colored_text("<!> Сбой в работе системы", Fore.RED)

def start_game_over():
    clear_terminal(False)
    print_colored_text("> Критическое повреждение базовой системы", Fore.RED)
    for _ in range(3):
        print_random_system_error_text()
    pause(1)
    print_colored_text("> Сбой работы двигателей", Fore.YELLOW)
    for _ in range(3):
        print_random_system_error_text()
    pause(0.5)
    print_colored_text("> Сбой системы подачи кислорода", Fore.YELLOW)
    for _ in range(3):
        print_random_system_error_text()
    pause(0.5)
    print_colored_text("> Сбой системы жизнеобеспечения", Fore.RED)
    for _ in range(4):
        print_random_system_error_text()
    pause(1)
    print_colored_text("> Нарушение целостности корабля", Fore.RED)
    pause(0.5)
    for _ in range(3):
        print_random_system_error_text()
    print_colored_text("> Отключение", Fore.RED)
    for n in range(10):
        print("\r[" + "=" * n + "]", end="", flush=True)
        pause(0.25)
    print(Back.RESET + Fore.RESET)


def run_game_over_screen():
    start_game_over()
    clear_terminal(False)
    print_colored_text("Игра завершена. Ваш корабль уничтожен.\n\nНажмите любую клавишу для продолжения.")
    keyboard.read_key()
    clear_terminal(False)
    main_menu.run_main_menu()
