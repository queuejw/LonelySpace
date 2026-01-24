import json

import colorama

from base.core import components, constants
from base.game.classes.base.game_event import GameEvent
from base.game.classes.planet.planet import Planet


# Загружает список планет из json файла и возвращает его.
def load_planets(path: str) -> list[Planet]:
    # Возвращает список с событиями на планете. Если событий нет, возвращает пустой список
    def load_events_list(d: dict) -> list[GameEvent]:
        try:
            planet_event = d['events']
        except KeyError:
            if components.SETTINGS.get_debug_mode():
                print(f"Ошибка при загрузке событий для планеты {d['name']}, используется пустой список.")
            return []
        return [
            GameEvent(item['name'], item['description'], list(item['commands']), float(item['prob']), item['color'])
            for item in planet_event]

    if components.SETTINGS.get_debug_mode():
        print(f"Попытка загрузить планеты из файла {path}")
    try:
        with open(path, 'r', encoding="utf-8") as planets_file:
            try:
                planets = json.load(planets_file)
                planets_file.close()
            # Если по каким-то причинам не удалось прочитать файл, возвращаем пустой список
            except json.JSONDecodeError:
                print(
                    f"{colorama.Fore.RED}[E] Не удалось прочитать файл {path}")
                return []
            if components.SETTINGS.get_debug_mode():
                print(f"Планеты успешно загружены, создание списка ...")
            custom_planet = path == constants.CUSTOM_PLANETS_FILE_PATH
            gen_list = []
            if len(planets) < 1:
                print(
                    f"{colorama.Fore.RED}[E] Планеты не найдены, возвращаю пустой список.")
                return []
            for m in planets:
                try:
                    planet = Planet(m['id'], m['name'], m['description'], m['type'], m['danger'], m['eta'],
                                    m['temperature'], load_events_list(m),
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
