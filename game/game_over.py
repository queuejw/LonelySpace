import keyboard
from colorama import Fore, Back

from core.console_manager import clear_terminal, print_colored_text
from core.core_utils import pause
from core.menus import main_menu


def start_game_over():
    clear_terminal(False)
    print_colored_text("> Критическое повреждение базовой системы", Fore.RED)
    print_colored_text("<!> Сбой в работе системы", Fore.RED)
    pause(1)
    print_colored_text("> Сбой работы двигателей", Fore.YELLOW)
    pause(0.5)
    print_colored_text("> Сбой системы подачи кислорода", Fore.YELLOW)
    print_colored_text("<!> Сбой в работе системы", Fore.RED)
    print_colored_text("<!> Сбой в работе системы", Fore.RED)
    pause(0.5)
    print_colored_text("> Сбой системы жизнеобеспечения", Fore.RED)
    print_colored_text("<!> Сбой в работе системы", Fore.RED)
    pause(1)
    print_colored_text("> Нарушение целостности корабля", Fore.RED)
    pause(0.5)
    print_colored_text("<!> Сбой в работе системы", Fore.RED)
    print_colored_text("> Отключение", Fore.RED)
    for n in range(10):
        print("\r[" + "=" * n + "]", end="", flush=True)
        pause(0.25)
    print(Back.RESET + Fore.RESET)


def run_game_over_screen():
    start_game_over()
    clear_terminal(True)
    print_colored_text("Игра завершена. Ваш корабль уничтожен.\n\nНажмите любую клавишу для продолжения.")
    keyboard.read_key()
    clear_terminal(False)
    main_menu.run_main_menu()
