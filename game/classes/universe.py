# Класс вселенной, игровой локации.

class Universe:
    def __init__(self, universe_name: str, planets_list: list, x: int, y: int):
        self.name = universe_name  # Название вселенной
        self.max_x = x  # Максимальное значение координат x, определяется по планетам.
        self.max_y = y  # Максимальное значение координат y, определяется по планетам.
        self.planets = planets_list  # Список планет на этой локации. Для оптимальной игры достаточно 30, но не более 100.
