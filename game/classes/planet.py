import random


# Класс планеты.
class Planet:
    def __init__(self, planet_name: str):
        self.name = planet_name  # Название планеты, указывается при создании
        self.x = round(
            random.random() / random.random() * 1000)  # Положение планеты по координатам x, генерируется случайно
        self.y = round(
            random.random() / random.random() * 1000)  # Положение планеты по координатам y, генерируется случайно
        self.resources = random.randint(100,
                                        1000)  # Количество ресурсов на планете (игровая валюта), генерируется случайное число от 100 до 300.
