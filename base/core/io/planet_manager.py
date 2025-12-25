import json

import colorama

from base.core import components, constants
from base.game.classes.planet.planet import Planet


# Загружает список планет из json файла.
def load_planets(path: str) -> list[Planet]:
    if components.SETTINGS.get_debug_mode():
        print(f"Попытка загрузить планеты из файла {path}")
    try:
        with open(path, 'r', encoding="utf-8") as planets_file:
            planets = json.load(planets_file)
            planets_file.close()
            if components.SETTINGS.get_debug_mode():
                print(f"Планеты успешно загружены, создание списка ...")
            custom_planet = path == constants.CUSTOM_PLANETS_FILE_PATH
            generated_list = [
                Planet(m['id'], m['name'], m['description'], m['type'], m['danger'], m['eta'], m['temperature'],
                       custom_planet, '' if not custom_planet else m['author']) for m
                in planets]
            return generated_list
    except FileNotFoundError:
        print(
            f"{colorama.Fore.RED}[E] Файл {path}, который должен содержать планеты, не найден. Невозможно продолжить работу.")
        exit(1)
    except KeyError as e:
        print(
            f"{colorama.Fore.RED}[E] Файл {path}, который должен содержать планеты, содержит ошибки. Восстановите файл, либо свяжитесь с нами.\n\nИнформация: {e}")
        exit(1)
