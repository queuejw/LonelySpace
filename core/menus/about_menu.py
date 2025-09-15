import keyboard as kb

from core.console_manager import print_colored_text, clear_terminal
from core.menus import main_menu
from core.translation_manager import TRANSLATIONS


def print_about_menu():
    # Создаем и отправляем текст параметров игры
    print_colored_text(TRANSLATIONS['about_text'])


def about_menu_input():
    # Ожидаем ввод игрока
    keycode = kb.read_key()
    # Выполняем действие в зависимости от выбора игра. Если действие неизвестно, уведомляем игрока и ждем новое действие.
    if keycode != "enter":
        about_menu_input()
    else:
        clear_terminal()
        main_menu.run_main_menu()


# Функция, которая обрабатывает меню "авторы игры"
def run_about_menu():
    clear_terminal()
    print_about_menu()
    about_menu_input()
