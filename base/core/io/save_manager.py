import json
import os

from base.core.constants import DEBUG_MODE, SAVES_FILE_PATH, SAVES_FOLDER_NAME
from base.game.classes.ship import Ship


def create_random_name() -> str:
    return "TestPlane-20"


def get_default_ship() -> Ship:
    return Ship(create_random_name())


# Загружает состояние с диска. Если его нет, создает новый корабль. Возвращает словарь со значениями ship : Ship, default: bool
def load_ship_state() -> dict:
    if DEBUG_MODE:
        print(f"Попытка загрузить файл {SAVES_FILE_PATH}")
    try:
        with open(SAVES_FILE_PATH, 'r', encoding="utf-8") as save_file:
            state = json.load(save_file)
            save_file.close()
            if DEBUG_MODE:
                print(f"Файл {SAVES_FILE_PATH} успешно загружен")
                print(state)
            return {
                'default': False,
                'ship': Ship('loaded').import_from_dict(state)
            }
    except FileNotFoundError:
        if DEBUG_MODE:
            print(f"[E] Файл {SAVES_FILE_PATH} не найден. Используем стандартный корабль.")

    # Если загрузить не удалось, возвращаем стандартный корабль.
    default = get_default_ship()
    return {
        'default': True,
        'ship': default
    }


# Сохраняет состояние на диск
def save_ship_state(state: dict) -> bool:
    if DEBUG_MODE:
        print(f"Попытка сохранить на диск файл {SAVES_FILE_PATH}")
    try:
        os.makedirs(SAVES_FOLDER_NAME, exist_ok=True)
        with open(SAVES_FILE_PATH, 'w', encoding="utf-8") as save_file:
            save_file.write(json.dumps(state, indent=4, ensure_ascii=False))
            save_file.close()
        return True
    except IOError as e:
        if DEBUG_MODE:
            print(f"[E] По какой-то причине не удалось сохранить файл {SAVES_FILE_PATH}. Детали: {e}")
        return False
