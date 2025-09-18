import time

import keyboard as kb  # Библиотека keyboard, которая используется для получения нажатия клавиш.
from colorama import Back, Fore

from core import saves_manager
from core.console_manager import print_colored_text, slow_print_colored_text
from core.constants import DEBUG_MODE_ENABLED
from core.menus import settings_menu
from core.menus.about_menu import run_about_menu
from core.translation_manager import TRANSLATIONS
from game.game_init import init_survival_game


# Инициализирует запуск новой игры в зависимости от режима игры
def start_new_game(game_mode: str):
    if DEBUG_MODE_ENABLED:
        print(f"Запуск новой игры в режиме {game_mode}")
    match game_mode:
        case "survival":
            init_survival_game()
        case _:
            print_colored_text(TRANSLATIONS['game_launch_error'] + "Unknown game mode", Back.RED)


def load_previous_game():
    pass


# Выводит текст с предложением загрузить игру
def ask_to_load_game():
    print_colored_text(TRANSLATIONS['game_save_founded'])
    keycode = kb.read_key()
    if keycode == "y":
        load_previous_game()
    else:
        print_colored_text(TRANSLATIONS['game_loading_canceled'])
        main_menu_input()


# Проверяет сохранения и запускает игру
def init_game_launch():
    if saves_manager.save_exist():
        ask_to_load_game()
    else:
        start_new_game("survival")


# Обработка нажатия клавиши
def main_menu_key_code_check(code: str) -> bool:
    # Если включена отладка, выводит код клавиши.
    if DEBUG_MODE_ENABLED:
        print(code)

    match code:
        case '1':  # Начать новую игру, либо предложить продолжить прошлую, если есть такая.
            init_game_launch()
        case '2':  # Подключиться к серверу / Создать сервер для многопользовательской игры.
            print("2")
        case '3':  # Параметры игры
            settings_menu.run_settings_menu()
        case 'esc':  # Выход из игры
            slow_print_colored_text(Back.GREEN + TRANSLATIONS['exit_message'], delay=0.05, color=Fore.BLACK)
            print(Fore.RESET, Back.RESET)
            time.sleep(1)
            exit(0)
        case 'a':  # меню "Авторы игры"
            run_about_menu()
        case _:  # Неизвестное действие
            return False
    return True


# Функция, которая выводит текст главного меню.
def print_main_menu():
    # Создаем и отправляем текст главного меню игры
    print_colored_text(TRANSLATIONS['main_menu_message'])
    # Если включен режим отладки, уведомляем
    if DEBUG_MODE_ENABLED:
        print_colored_text(TRANSLATIONS['debug_mode_enabled'], Fore.RED)


# Функция, которая обрабатывает нажатия в главном меню
def main_menu_input():
    # Ожидаем ввод игрока
    keycode = kb.read_key()
    # Выполняем действие в зависимости от выбора игра. Если действие неизвестно, уведомляем игрока и ждем новое действие.
    if not main_menu_key_code_check(keycode):
        main_menu_input()


# Функция, которая обрабатывает главное меню игры
def run_main_menu():
    print_main_menu()
    main_menu_input()
