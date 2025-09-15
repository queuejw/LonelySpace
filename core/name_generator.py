import os
import random

from colorama import Back

from core.console_manager import print_colored_text
from core.translation_manager import TRANSLATIONS


# Создаёт случайное название для корабля
def create_random_ship_name() -> str:
    random_num = random.randint(1, 255)
    ships = [f"Dragon-{random_num}", f"Eagle-{random_num}"] + [f"{ship}-{random_num}" for ship in "XFGZ"]
    name = random.choice(ships)
    return name


# Загружает планеты в зависимости от языка
def load_planet_list(lang: str) -> list:
    file = os.path.join("planets", lang, "planets.txt")
    if os.path.exists(file):
        planets_list = []
        with open(file, encoding="utf-8") as f:
            for item in f.readlines():
                planets_list.append(item.replace("\n", ""))
        return planets_list
    else:
        print_colored_text(TRANSLATIONS['planets_error'], Back.RED)
        exit(2)
