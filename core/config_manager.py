import json
import os

from colorama import Back

from core import translation_manager
from core.console_manager import print_colored_text
from core.constants import DEFAULT_GAME_CONFIG, DEFAULT_CONFIG_NAME, DEBUG_MODE_ENABLED


# Возвращает стандартный конфиг
def create_default_config() -> dict:
    return DEFAULT_GAME_CONFIG


# Функция, которая загружает конфигурацию игры из файла.
def load_config() -> dict:
    if DEBUG_MODE_ENABLED:
        print("Загрузка файла конфигурации")
    # Получаем путь к файлу
    file = os.path.join(DEFAULT_CONFIG_NAME)
    if os.path.exists(file):
        # Если файл существует, открываем его и сохраняем значения в переменной CONFIG
        with open(file, encoding="utf-8") as f:
            config_json = json.load(f)
            if DEBUG_MODE_ENABLED:
                print(config_json)
            return config_json
    else:
        # Если файл не существует, создаём новый и используем стандартный конфиг.
        if DEBUG_MODE_ENABLED:
            print("Файл не найден, создаём новый.")
        default_config = create_default_config()
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(default_config, indent=4, ensure_ascii=True))

        return default_config


# Функция, которая перезаписывает файл конфигурации на новый
def update_config(new_config):
    file = os.path.join(DEFAULT_CONFIG_NAME)
    if os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(new_config, indent=4, ensure_ascii=True))
            if DEBUG_MODE_ENABLED:
                print("Файл конфигурации обновлён")
    else:
        if DEBUG_MODE_ENABLED:
            print("Не удалось сохранить конфиг")
        print_colored_text(translation_manager.TRANSLATIONS['config_save_error'], Back.RED)

    global CONFIG
    CONFIG = new_config


# Конфигурация игры
CONFIG = load_config()
