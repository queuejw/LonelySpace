import json

import colorama

from base.core import components, constants
from base.game.classes.planet.planet import Planet
from base.game.classes.planet.planet_event import PlanetEvent


# Загружает список планет из json файла.
def load_planets(path: str) -> list[Planet]:

    def load_events_list(d: list[dict]) -> list[PlanetEvent]:
        return [PlanetEvent(item['name'], item['description'], list(item['commands']), float(item['prob'])) for item in d]

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
                Planet(m['id'], m['name'], m['description'], m['type'], m['danger'], m['eta'], m['temperature'], load_events_list(m['events']),
                       custom_planet, constants.PRODUCT_NAME if not custom_planet else m['author']) for m
                in planets]
            return generated_list
    except FileNotFoundError:
        print(
            f"{colorama.Fore.RED}[E] Файл {path}, который должен содержать планеты, не найден. Невозможно продолжить работу.")
        components.ENGINE.running = False
        return []
    except KeyError as e:
        print(
            f"{colorama.Fore.RED}[E] Файл {path}, который должен содержать планеты, содержит ошибки. Восстановите файл, либо свяжитесь с нами.\n\nИнформация: {e}")
        return []
