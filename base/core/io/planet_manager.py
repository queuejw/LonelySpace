import json

from base.core.constants import DEBUG_MODE, PLANETS_FILE_PATH
from base.game.classes.planet import Planet


# Загружает список планет из json файла.
def load_planets() -> list:
    if DEBUG_MODE:
        print(f"Попытка загрузить планеты из файла {PLANETS_FILE_PATH}")
    try:
        with open(PLANETS_FILE_PATH, 'r', encoding="utf-8") as planets_file:
            planets = json.load(planets_file)
            planets_file.close()
            if DEBUG_MODE:
                print(f"Планеты успешно загружены, создание списка ...")

            generated_list = [
                Planet(m['id'], m['name'], m['description'], m['type'], m['danger'], m['eta'], m['temperature']) for m
                in planets]
            return generated_list
    except FileNotFoundError:
        print(
            f"[E] Файл {PLANETS_FILE_PATH}, который должен содержать планеты, не найден. Невозможно продолжить работу.")
        exit(1)
