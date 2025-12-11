import colorama

from base.core import constants
from base.core.console import clear_terminal, slow_print
from base.core.constants import PRODUCT_NAME, DEBUG_MODE, PRODUCT_GITHUB_LINK
from base.game.classes.ui.base.screen import ScreenBase
from base.game.classes.ui.game_screen import GameScreen


def get_ship_drawing(level: int) -> str:
    from base.core.io.txt_loader import load_txt_file
    match level:
        case 0:
            return load_txt_file("base\\game\\res\\ship.txt")
        case _:
            return "error"


def init_game_launch(skip: bool = False):
    clear_terminal()
    from base.core.io import save_manager
    loaded_data = save_manager.load_ship_state()
    # Выводим забавные сообщения, которые никак не влияют на игру
    if not skip:
        if not loaded_data['default']:
            print(colorama.Back.GREEN + colorama.Fore.BLACK + "Вы продолжите игру с последнего сохранения")
        from playsound3 import playsound
        sound1 = playsound("base//game//res//audio//starting_basic_systems.mp3", False)
        slow_print("Запуск базовых систем ...", colorama.Fore.GREEN)
        import time
        time.sleep(1)
        sound2 = playsound("base//game//res//audio//loading_firmware.mp3", False)
        slow_print("Загрузка прошивки ...", colorama.Fore.GREEN)
        time.sleep(1)
        sound2 = playsound("base//game//res//audio//checking_basic_systems.mp3", False)
        slow_print("Проверка базовых систем ...", colorama.Fore.GREEN)
        time.sleep(2)
        print(
            colorama.Fore.YELLOW + "Внимание: Автоматическая система диагностики обнаружила проблемы с безопасностью. Запущен глубокий анализ.")
        sound3 = playsound("base//game//res//audio//starting_hardware.mp3", False)
        slow_print("Запуск оборудования ...", colorama.Fore.GREEN)
        time.sleep(1)
        print(colorama.Fore.YELLOW + "-> Проверка системы жизнеобеспечения ...", end='\r')
        time.sleep(0.5)
        print(colorama.Fore.YELLOW + "-> Оптимизация системы навигации", end='\r')
        time.sleep(0.8)
        print(colorama.Fore.YELLOW + "-> Обновление параметров системы ...", end='\r')
        time.sleep(0.2)
        print(colorama.Fore.YELLOW + "-> Очистка временных файлов базовой системы ...", end='\r')
        time.sleep(0.2)
        print(colorama.Fore.GREEN + "-> Завершено" + " " * 40)
        sound4 = playsound("base//game//res//audio//starting_ui.mp3", False)
        slow_print("Подготовка пользовательского интерфейса ...", colorama.Fore.GREEN)
        time.sleep(1.5)
        sound5 = playsound("base//game//res//audio//init_user_space.mp3", False)
        slow_print("Инициализация пространства пользователя ...", colorama.Fore.GREEN)
        print(colorama.Fore.RED + "Ошибка: Обнаружена критическая уязвимость в системе безопасности.")
        time.sleep(0.1)
        print(colorama.Fore.RED + "Ошибка: Сертификаты безопасности устарели")
        time.sleep(0.25)
        print(colorama.Fore.RED + "Ошибка: Отсутствует спасательная капсула")
        time.sleep(0.3)
        print(colorama.Fore.RED + "Ошибка: Система фильтрации воздуха имеет неисправимые повреждения")
        time.sleep(0.75)
        print(colorama.Fore.CYAN + "Неизвестный пользователь: Предупреждения об угрозах безопасности отключены.")
        time.sleep(0.3)
        clear_terminal()
        print(colorama.Fore.GREEN + "Все системы в рабочем состоянии.")
        sound6 = playsound("base//game//res//audio//systems_ready.mp3", True)
        del sound1
        del sound2
        del sound3
        del sound4
        del sound5
        del sound6
        clear_terminal()

    # Здесь по факту происходит запуск игры.
    from base.core import components
    components.GAME.player = loaded_data['ship']
    components.GAME.player_drawing = get_ship_drawing(loaded_data['ship'].level)
    from base.core.io import planet_manager
    components.GAME.planets = planet_manager.load_planets()
    # Помечаем игру как запущенную
    components.GAME.running = True
    # Блокируем ввод.
    components.ENGINE.pending_input = False
    components.GAME.last_messages.clear()
    components.GAME.update_last_messages(f"Добро пожаловать в {constants.PRODUCT_NAME}!")
    del loaded_data

    # Возвращаем экран игры.
    return GameScreen()


class MainMenu(ScreenBase):

    def render(self):
        clear_terminal()
        text = (
            f"{colorama.Fore.GREEN}Добро пожаловать в {colorama.Fore.CYAN}{PRODUCT_NAME}\n\n"
            f"{colorama.Fore.CYAN}start {colorama.Fore.GREEN}- Начать игру\n"
            f"{colorama.Fore.CYAN}info {colorama.Fore.GREEN}- Об игре\n"
            f"{colorama.Fore.CYAN}exit {colorama.Fore.GREEN}- Закрыть игру\n\n"
            f"{colorama.Fore.GREEN}Введите команду в терминал:\n"
        )
        print(text)

    def handle_input(self, command: str):
        match command:
            case "start":
                if DEBUG_MODE:
                    print("Ожидается запуск игры")
                return init_game_launch(DEBUG_MODE)
            case "info":
                t = (
                    f"{colorama.Fore.CYAN}{PRODUCT_NAME}{colorama.Fore.GREEN} - игра про космос на Python, которая разрабатывается в свободное время небольшой командой разработчиков.\n\n"
                    f"{colorama.Fore.CYAN}@pxffd{colorama.Fore.GREEN} - Автор идеи и главный разработчик\n"
                    f"{colorama.Fore.CYAN}неизвестный фанат{colorama.Fore.GREEN} - Автор обложки игры.\n\n"
                    f"{colorama.Fore.CYAN}{PRODUCT_GITHUB_LINK}{colorama.Fore.GREEN} - Исходный код игры и обратная связь.\n"
                    f"[РЕКЛАМА] {colorama.Fore.CYAN}https://t.me/mars_1323{colorama.Fore.GREEN} - мой тематический чат в Telegram про Марс"
                )
                print(t)
                del t
            case "exit":
                if DEBUG_MODE:
                    print("Ожидается выход из игры")
                slow_print("Отключение базовых систем...", colorama.Fore.GREEN)
                from base.core import components
                components.ENGINE.stop()
            case _:
                print(colorama.Fore.RED + "Неизвестная команда.")

        return self

    def update(self):
        pass
