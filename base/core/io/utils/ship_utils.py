from base.game.classes.ship.ship import Ship


# Возвращает случайное название для корабля
def create_random_name() -> str:
    import random
    names = ["Спутник-", "Марс-", "Луна-", "F-", "G-"]
    return f"{random.choice(names)}{random.randint(1, 999)}"


# Возвращает стандартный корабль
def get_default_ship() -> Ship:
    return Ship(create_random_name())
