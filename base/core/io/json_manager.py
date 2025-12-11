import json
import os

from base.core.constants import DEBUG_MODE, SAVE_FILE_PATH, SETTINGS_FILE_PATH
from base.core.io.utils.settings_utils import get_default_settings_file


# Загружает содержимое json с диска.
# Если это сохранение, возвращает словарь со значениями ship : Ship, default: bool
def load_file(path: str) -> dict:
    if DEBUG_MODE:
        print(f"Попытка загрузить файл {path}")
    try:
        with open(path, 'r', encoding="utf-8") as file:
            loaded_json: dict = json.load(file)
            file.close()
            if DEBUG_MODE:
                print(f"Файл {path} успешно загружен")
                print(loaded_json)
            if path == SAVE_FILE_PATH:
                from base.game.classes.ship import Ship
                return {
                    'default': False,
                    'ship': Ship('loaded').import_from_dict(loaded_json)
                }
            else:
                return loaded_json
    except FileNotFoundError:
        if DEBUG_MODE:
            print(f"[E] Файл {SAVE_FILE_PATH} не найден.")

    # Если загрузить не удалось, возвращаем стандартное значение.
    if path == SAVE_FILE_PATH:
        from base.core.io.utils.ship_utils import get_default_ship
        return {
            'default': True,
            'ship': get_default_ship()
        }
    elif path == SETTINGS_FILE_PATH:
        return get_default_settings_file()
    else:
        return {

        }


# Сохраняет содержимое словаря на диск в виде JSON
def save_file(state: dict, path: str, folder: str) -> bool:
    if DEBUG_MODE:
        print(f"Попытка сохранить на диск файл {path}")
    try:
        os.makedirs(folder, exist_ok=True)
        with open(path, 'w', encoding="utf-8") as file:
            file.write(json.dumps(state, indent=4, ensure_ascii=False))
            file.close()
        return True
    except IOError as e:
        if DEBUG_MODE:
            print(f"[E] По какой-то причине не удалось сохранить файл {path}. Детали: {e}")
        return False
