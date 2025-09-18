import json
import os

from colorama import Back, Fore

from core.config_manager import CONFIG
from core.console_manager import print_colored_text
from core.constants import DEBUG_MODE_ENABLED


# Функция, которая загружает файл локализации в память.
def load_translations(code: str) -> dict:
    file = os.path.join("lang", f"{code}.json")
    if DEBUG_MODE_ENABLED:
        print(f"Загрузка локализаций. Текущий язык: {code}. Файл: {file}")
    if os.path.exists(file):
        with open(file, encoding="utf-8") as f:
            translations_json = json.load(f)
            if DEBUG_MODE_ENABLED:
                print("Локализация загружена.")
            return translations_json
    else:
        print_colored_text(
            Fore.BLACK + "Unable to continue game launch. Check lang folder, maybe translation files broken or missing.",
            Back.RED)
        exit(1)


# Переменная, которая хранит все строки.
TRANSLATIONS = load_translations(CONFIG['lang'])


def reload_translations(code: str):
    if DEBUG_MODE_ENABLED:
        print("Перезагрузка системы локализаций")
    global TRANSLATIONS
    TRANSLATIONS = load_translations(code)
