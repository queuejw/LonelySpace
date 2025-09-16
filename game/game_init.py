import random

from core.config_manager import CONFIG
from core.console_manager import clear_terminal, slow_print_colored_text, print_colored_text
from core.constants import DEBUG_MODE_ENABLED
from core.core_utils import pause
from core.name_generator import load_planet_list, create_random_ship_name
from game import game_main, game_vars
from game.classes.planet import Planet
from game.classes.ship import PlayerShip
from game.classes.universe import Universe


# Создает список планет
def create_planets(num: int) -> list:
    if DEBUG_MODE_ENABLED:
        print("Генерация списка планет")

    planet_names = load_planet_list(CONFIG['lang'])  # Получаем имена
    result = [Planet(random.choice(planet_names)) for _ in range(num)]  # Создаем планеты со случайными названиями

    # Выводит некоторую информацию о планетах в режиме отладки.
    if DEBUG_MODE_ENABLED:
        print(*planet_names)
        print([x.name for x in result])
        print([planet.x for planet in result])
        print([planet.y for planet in result])

    # Возвращает итоговый список
    return result


# Возвращает новую вселенную
def create_universe(planets_list: list) -> Universe:
    if DEBUG_MODE_ENABLED:
        print("Создание вселенной")

    max_x = max([planet.x for planet in planets_list])  # Максимальное значение x на основе данных планет
    max_y = max([planet.y for planet in planets_list])  # Максимальное значение y на основе данных планет
    name = "Universe1"

    result = Universe(name, planets_list, max_x, max_y)
    # Некоторая информация о вселенной
    if DEBUG_MODE_ENABLED:
        print(result.name)
        print(result.max_x)
        print(result.max_y)
    return result


# Создает корабль игрока
def create_player() -> PlayerShip:
    ship_name = create_random_ship_name()
    result = PlayerShip(ship_name)
    # Выводит информацию о корабле в режиме отладки
    if DEBUG_MODE_ENABLED:
        print(result.name)
        print(result.speed)
        print(result.x)
        print(result.y)
        print(result.health)
        print(result.resources)
    # Возвращает корабль
    return result


def init_survival_game():
    clear_terminal()
    if not DEBUG_MODE_ENABLED:
        slow_print_colored_text("Идёт загрузка...\n", 0.2)
        print_colored_text("> Генерация космического пространства ...")
    # Создание локации
    m_planets = create_planets(20)  # Генерируем планеты
    game_vars.UNIVERSE = create_universe(m_planets)  # Создаем вселенную с этими планетами.
    # Искусственное замедление запуска

    # Если режим отладки включен, пропускаем это.
    if not DEBUG_MODE_ENABLED:
        print_colored_text("> Оптимизация путей ...")
        pause(1)
        print_colored_text("> Обновление прошивки ...")
        pause(1)
        print_colored_text("> Подготовка к запуску ...")
        pause(1)
    # Конец искусственного замедления, перейдем к делу.
    # Создание игрока
    game_vars.PLAYER = create_player()

    # Запускаем интерфейс, наконец-то.
    game_main.run_game_gui()
