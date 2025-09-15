import keyboard as kb

from core import translation_manager
from core.config_manager import CONFIG, update_config
from core.console_manager import clear_terminal, print_colored_text
from core.constants import DEBUG_MODE_ENABLED
from core.menu_shared_functions import menu_unknown_key_code
from core.menus import main_menu


# Возвращает название языка по его коду
def get_lang_name(code: str) -> str:
    match code:
        case "en":
            return "English"
        case "ru":
            return "Русский"
        case _:
            return "Unknown"


# Возвращает название сложности игры по её коду
def get_difficulty_name(code: int) -> str:
    match code:
        case 1:
            return translation_manager.TRANSLATIONS['difficulty_hard']
        case 0:
            return translation_manager.TRANSLATIONS['difficulty_normal']
        case _:
            return "Unknown"


# Изменение сложности игры
def change_difficulty():
    # Получаем значение из файла конфигурации
    current_value = CONFIG['difficulty']
    if DEBUG_MODE_ENABLED:
        print(f"Изменяем сложность. Текущая: {current_value}")
    # Изменяем в зависимости от значения.
    match current_value:
        case 0:
            # Нормальная -> Сложная
            new_value = 1
            CONFIG['difficulty'] = new_value
            update_config(CONFIG)
            if DEBUG_MODE_ENABLED:
                print(f"Новая сложность: {new_value}")
        case 1:
            # Сложная -> Нормальная
            new_value = 0
            CONFIG['difficulty'] = new_value
            update_config(CONFIG)
            if DEBUG_MODE_ENABLED:
                print(f"Новая сложность: {new_value}")
        case _:
            # ??? -> Нормальная
            # Этого не должно случиться, но я это предусмотрел.
            new_value = 0
            CONFIG['difficulty'] = new_value
            update_config(CONFIG)
            if DEBUG_MODE_ENABLED:
                print(f"Нестандартная ситуация, изменяю сложность на значение по умолчанию: {new_value}")

    run_settings_menu()


# Изменение языка игры
def change_language():
    # Получаем значение из файла конфигурации
    current_value = CONFIG['lang']
    if DEBUG_MODE_ENABLED:
        print(f"Изменяем язык. Текущий: {current_value}")
    # Изменяем в зависимости от значения.
    match current_value:
        case "en":
            # Английский -> Русский
            new_value = "ru"
            CONFIG['lang'] = new_value
            update_config(CONFIG)
            if DEBUG_MODE_ENABLED:
                print(f"Новый язык: {new_value}")
        case 1:
            # Русский -> Английский
            new_value = "en"
            CONFIG['lang'] = new_value
            update_config(CONFIG)
            if DEBUG_MODE_ENABLED:
                print(f"Новый язык: {new_value}")
        case _:
            # ??? -> Английский
            # Этого не должно случиться, но я это тоже предусмотрел.
            new_value = "en"
            CONFIG['lang'] = new_value
            update_config(CONFIG)
            if DEBUG_MODE_ENABLED:
                print(f"Нестандартная ситуация, изменяю язык на значение по умолчанию: {new_value}")

    if DEBUG_MODE_ENABLED:
        print(f"Изменён язык, обновляю текст. Язык в файле конфигурации: {CONFIG['lang']}")
    translation_manager.reload_translations(CONFIG['lang'])
    run_settings_menu()


# Обработка нажатия клавиши
def settings_menu_key_code_check(code: str) -> bool:
    # Если включена отладка, выводит код клавиши.
    if DEBUG_MODE_ENABLED:
        print(code)

    match code:
        # Изменить сложность
        case '1':
            change_difficulty()
        # Изменить язык
        case '2':
            change_language()
        # Параметры игры
        case 'enter':
            clear_terminal()
            main_menu.run_main_menu()
        # Неизвестное действие, уведомляем игрока
        case _:
            menu_unknown_key_code()
            return False
    return True


def print_settings_menu():
    # Создаем и отправляем текст параметров игры
    print_colored_text(translation_manager.TRANSLATIONS['settings_message'])
    print_colored_text("=====")
    print_colored_text(
        translation_manager.TRANSLATIONS['current_difficulty'] + get_difficulty_name(CONFIG['difficulty']))
    print_colored_text(translation_manager.TRANSLATIONS['current_lang'] + get_lang_name(CONFIG['lang']))


def settings_menu_input():
    # Ожидаем ввод игрока
    keycode = kb.read_key()
    # Выполняем действие в зависимости от выбора игра. Если действие неизвестно, уведомляем игрока и ждем новое действие.
    if not settings_menu_key_code_check(keycode):
        settings_menu_input()


# Функция, которая обрабатывает параметры игры
def run_settings_menu():
    clear_terminal()
    print_settings_menu()
    settings_menu_input()
