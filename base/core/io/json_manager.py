import json
import os

from base.core import components
from base.core.constants import SAVE_FILE_PATH, SETTINGS_FILE_PATH
from base.core.io.utils.settings_utils import get_default_settings_file


# Загружает содержимое json с диска.
# Если это сохранение игрока, возвращает словарь со значениями ship : Ship, default: bool
def load_file(path: str, skip_debug_prints: bool = False) -> dict:
    if not skip_debug_prints:
        if components.SETTINGS.get_debug_mode():
            print(f"Попытка загрузить файл {path}")
    try:
        with open(path, 'r', encoding="utf-8") as file:
            loaded_json: dict = json.load(file)
            file.close()
            if not skip_debug_prints:
                if components.SETTINGS.get_debug_mode():
                    print(f"Файл {path} успешно загружен")
                    print(loaded_json)
            if path == SAVE_FILE_PATH:
                from base.game.classes.ship.ship import Ship
                return {
                    'default': False,
                    'ship': Ship('loaded').import_from_dict(loaded_json)
                }
            else:
                return loaded_json
    except FileNotFoundError:
        if not skip_debug_prints:
            if components.SETTINGS.get_debug_mode():
                print(f"[E] Файл {SAVE_FILE_PATH} не найден.")

    # Если загрузить не удалось, возвращаем стандартное значение.
    if path == SAVE_FILE_PATH:
        from base.core.io.utils.ship_utils import get_default_ship
        # Стандартный корабль
        return {
            'default': True,
            'ship': get_default_ship()
        }
    elif path == SETTINGS_FILE_PATH:
        # Стандартные настройки
        return get_default_settings_file()
    else:
        # А тут ничего.
        return {
            # Здесь ничего нет
        }


# Сохраняет содержимое словаря на диск в виде JSON
def save_file(state: dict, path: str, folder: str) -> bool:
    if components.SETTINGS.get_debug_mode():
        print(f"Попытка сохранить на диск файл {path}")
    try:
        # Создаём директорию {folder}, если её нет.
        os.makedirs(folder, exist_ok=True)
        with open(path, 'w', encoding="utf-8") as file:
            # Сохраняем файл на диске
            file.write(json.dumps(state, indent=4, ensure_ascii=False))
            file.close()
        return True
    except IOError as e:
        if components.SETTINGS.get_debug_mode():
            print(f"[E] По какой-то причине не удалось сохранить файл {path}. Детали: {e}")
        return False
