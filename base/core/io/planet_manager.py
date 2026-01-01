import json

import colorama

from base.core import components, constants
from base.game.classes.planet.planet import Planet
from base.game.classes.planet.planet_event import PlanetEvent


# Загружает список планет из json файла и возвращает его.
def load_planets(path: str) -> list[Planet]:
    # Возвращает список с событиями на планете.
    def load_events_list(d: list[dict]) -> list[PlanetEvent]:
        return [
            PlanetEvent(item['name'], item['description'], list(item['commands']), float(item['prob']), item['color'])
            for item in d]

    if components.SETTINGS.get_debug_mode():
        print(f"Попытка загрузить планеты из файла {path}")
    try:
        path = path.replace("\\","/") #линукс совместимость
        with open(path, 'r', encoding="utf-8") as planets_file:
            planets = json.load(planets_file)
            planets_file.close()
            if components.SETTINGS.get_debug_mode():
                print(f"Планеты успешно загружены, создание списка ...")
            custom_planet = path == constants.CUSTOM_PLANETS_FILE_PATH
            gen_list = []
            for m in planets:
                try:
                    planet = Planet(m['id'], m['name'], m['description'], m['type'], m['danger'], m['eta'],
                                    m['temperature'], load_events_list(m['events']),
                                    custom_planet, constants.PRODUCT_NAME if not custom_planet else m['author'])
                    gen_list.append(planet)
                    del planet
                except KeyError as e:
                    print(f"{colorama.Fore.RED}Ошибка при загрузке планеты: {e}")

            return gen_list
    except FileNotFoundError:
        print(
            f"{colorama.Fore.RED}[E] Файл {path}, который должен содержать планеты, не найден. Невозможно продолжить работу.")
        components.ENGINE.running = False
        return []
