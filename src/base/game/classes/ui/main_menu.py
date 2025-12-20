import colorama
import playsound3

from base.core import components
from base.core import constants
from base.core.console import clear_terminal, slow_print
from base.core.constants import PRODUCT_NAME, PRODUCT_GITHUB_LINK
from base.core.io.json_manager import save_file
from base.game.classes.ui.base.screen import ScreenBase
from base.game.classes.ui.game_screen import GameScreen


# Симуляция запуска игры, возвращает экран игры.
def init_game_launch(skip: bool = False):
    clear_terminal()
    from base.core import components
    from base.core.io import json_manager
    loaded_data = json_manager.load_file(constants.SAVE_FILE_PATH)
    # Выводим забавные сообщения, которые никак не влияют на игру
    if not skip:
        if not loaded_data['default']:
            print(colorama.Back.GREEN + colorama.Fore.BLACK + "Вы продолжите игру с последнего сохранения")
        from playsound3 import playsound
        if components.SETTINGS.get_sound():
            sound1 = playsound("base//game//res//audio//starting_basic_systems.mp3", False)
        slow_print("Запуск базовых систем ...", colorama.Fore.GREEN)
        import time
        time.sleep(1)
        if components.SETTINGS.get_sound():
            sound2 = playsound("base//game//res//audio//loading_firmware.mp3", False)
        slow_print("Загрузка прошивки ...", colorama.Fore.GREEN)
        time.sleep(1)
        if components.SETTINGS.get_sound():
            sound2 = playsound("base//game//res//audio//checking_basic_systems.mp3", False)
        slow_print("Проверка базовых систем ...", colorama.Fore.GREEN)
        time.sleep(2)
        print(
            colorama.Fore.YELLOW + "Внимание: Автоматическая система диагностики обнаружила проблемы с безопасностью. Запущен глубокий анализ.")
        if components.SETTINGS.get_sound():
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
        if components.SETTINGS.get_sound():
            sound4 = playsound("base//game//res//audio//starting_ui.mp3", False)
        slow_print("Подготовка пользовательского интерфейса ...", colorama.Fore.GREEN)
        time.sleep(1.5)
        if components.SETTINGS.get_sound():
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
        if components.SETTINGS.get_sound():
            sound6 = playsound("base//game//res//audio//systems_ready.mp3", True)
            del sound1
            del sound2
            del sound3
            del sound4
            del sound5
            del sound6
        if components.SETTINGS.get_sound():
            components.GAME.add_audio_to_queue("base//game//res//audio//welcome.mp3")
        clear_terminal()

    # Здесь по факту происходит запуск игры.
    components.GAME.player = loaded_data['ship']
    from base.core.io.txt_loader import load_txt_file
    components.GAME.player_in_space_drawing = load_txt_file("base//game//res//txt//ship_in_space.txt")
    components.GAME.player_on_planet_drawing = load_txt_file("base//game//res//txt//ship_on_planet.txt")
    from base.core.io import planet_manager
    components.GAME.planets = planet_manager.load_planets(constants.PLANETS_FILE_PATH)
    # Если планеты сообщества включены, добавляем их в общий список планет.
    if components.SETTINGS.get_custom_planets_support():
        components.GAME.planets += planet_manager.load_planets(constants.CUSTOM_PLANETS_FILE_PATH)
    # Помечаем игру как запущенную
    components.GAME.running = True
    # Блокируем ввод.
    components.ENGINE.pending_input = False
    components.GAME.last_messages.clear()
    components.GAME.update_last_messages(f"Добро пожаловать в {constants.PRODUCT_NAME}!")

    # НА ВРЕМЯ БЕТА ТЕСТА
    components.GAME.update_last_messages(f"GitHub проекта: {constants.PRODUCT_GITHUB_LINK}")

    del loaded_data

    # Возвращаем экран игры.
    return GameScreen()


# Возвращает название языка по его коду
def get_lang_name(value: str) -> str:
    match value:
        case 'ru':
            return "Русский"
        case 'en':
            return "English"
        case _:
            return "Unknown"


class MainMenu(ScreenBase):

    def render(self):
        clear_terminal()
        text = (
            f"{colorama.Fore.GREEN}Добро пожаловать в {colorama.Fore.CYAN}{PRODUCT_NAME}\n\n"
            f"{colorama.Fore.CYAN}start {colorama.Fore.GREEN}- Начать игру\n"
            f"{colorama.Fore.CYAN}settings {colorama.Fore.GREEN}- Настроить игру\n\n"
            f"{colorama.Fore.CYAN}info {colorama.Fore.GREEN}- Об игре\n"
            f"{colorama.Fore.CYAN}exit {colorama.Fore.GREEN}- Закрыть игру\n\n"
            f"{colorama.Fore.GREEN}Введите команду в терминал:\n"
        )
        print(text)
        del text

    def handle_input(self, command: str):

        command = command.split()

        # Эта функция отвечает за управление настройками
        def handle_settings_command(user_command: list[str]):
            if len(user_command) == 3:
                match user_command[1]:
                    case 'lang':
                        new_lang = user_command[2]
                        # Если язык есть в списке доступных.
                        if new_lang in ['ru', 'en']:
                            components.SETTINGS.lang = new_lang
                            save_file(components.SETTINGS.export_as_dict(), constants.SETTINGS_FILE_PATH,
                                      constants.USER_FOLDER_NAME)
                            if components.SETTINGS.sound:
                                playsound3.playsound("base//game//res//audio//command_executed.mp3", False)
                            print(
                                f"{colorama.Fore.GREEN}Язык успешно изменен. Перезапустите игру, чтобы полностью изменить его.")
                        else:
                            if components.SETTINGS.sound:
                                playsound3.playsound("base//game//res//audio//command_handle_error.mp3", False)
                            print(
                                f"{colorama.Fore.RED}Этот язык не поддерживается игрой.")
                        del new_lang
                    case 'sound':
                        new_sound_value = user_command[2]
                        if new_sound_value == '1':
                            components.SETTINGS.sound = True
                            save_file(components.SETTINGS.export_as_dict(), constants.SETTINGS_FILE_PATH,
                                      constants.USER_FOLDER_NAME)
                            if components.SETTINGS.sound:
                                playsound3.playsound("base//game//res//audio//command_executed.mp3", False)
                            print(
                                f"{colorama.Fore.GREEN}Звук включен. Перезапустите игру, чтобы полностью применить изменения.")
                        elif new_sound_value == '0':
                            components.SETTINGS.sound = False
                            save_file(components.SETTINGS.export_as_dict(), constants.SETTINGS_FILE_PATH,
                                      constants.USER_FOLDER_NAME)
                            print(
                                f"{colorama.Fore.GREEN}Звук отключен. Перезапустите игру, чтобы полностью применить изменения.")
                        else:
                            if components.SETTINGS.sound:
                                playsound3.playsound("base//game//res//audio//invalid_argument.mp3", False)
                            print(
                                f"{colorama.Fore.RED}Недопустимое значение для аргумента sound.")
                        del new_sound_value
                    case 'debug':
                        new_debug_value = user_command[2]
                        if new_debug_value == '1':
                            components.SETTINGS.debug_mode = True
                            save_file(components.SETTINGS.export_as_dict(), constants.SETTINGS_FILE_PATH,
                                      constants.USER_FOLDER_NAME)
                            if components.SETTINGS.sound:
                                playsound3.playsound("base//game//res//audio//command_executed.mp3", False)
                            print(
                                f"{colorama.Fore.GREEN}Режим отладки включен.")
                        elif new_debug_value == '0':
                            components.SETTINGS.debug_mode = False
                            save_file(components.SETTINGS.export_as_dict(), constants.SETTINGS_FILE_PATH,
                                      constants.USER_FOLDER_NAME)
                            if components.SETTINGS.sound:
                                playsound3.playsound("base//game//res//audio//command_executed.mp3", False)
                            print(
                                f"{colorama.Fore.GREEN}Режим отладки отключен.")
                        else:
                            if components.SETTINGS.sound:
                                playsound3.playsound("base//game//res//audio//invalid_argument.mp3", False)
                            print(
                                f"{colorama.Fore.RED}Недопустимое значение для аргумента debug.")
                        del new_debug_value
                    case 'community':
                        new_community_value = user_command[2]
                        if new_community_value == '1':
                            components.SETTINGS.custom_planets = True
                            save_file(components.SETTINGS.export_as_dict(), constants.SETTINGS_FILE_PATH,
                                      constants.USER_FOLDER_NAME)
                            if components.SETTINGS.sound:
                                playsound3.playsound("base//game//res//audio//command_executed.mp3", False)
                            print(
                                f"{colorama.Fore.GREEN}Включены планеты сообщества.")
                        elif new_community_value == '0':
                            components.SETTINGS.custom_planets = False
                            save_file(components.SETTINGS.export_as_dict(), constants.SETTINGS_FILE_PATH,
                                      constants.USER_FOLDER_NAME)
                            if components.SETTINGS.sound:
                                playsound3.playsound("base//game//res//audio//command_executed.mp3", False)
                            print(
                                f"{colorama.Fore.GREEN}Отключены планеты сообщества.")
                        else:
                            if components.SETTINGS.sound:
                                playsound3.playsound("base//game//res//audio//invalid_argument.mp3", False)
                            print(
                                f"{colorama.Fore.RED}Недопустимое значение для аргумента debug.")
                        del new_community_value
            elif len(user_command) == 2:
                match user_command[1]:
                    case 'lang':
                        t = (
                            f"Доступные языки: {colorama.Fore.CYAN}ru{colorama.Fore.GREEN}\n"
                            f"{colorama.Fore.CYAN}settings lang [код]{colorama.Fore.GREEN} - смена языка по коду, которые вы увидите выше.\n"
                        )
                        print(t)
                        del t
                    case 'community':
                        print(
                            f"{colorama.Fore.CYAN}settings community [0 / 1]{colorama.Fore.GREEN} - планеты сообщества. 0 - отключить, 1 - включить.\n")
                    case 'sound':
                        print(
                            f"{colorama.Fore.CYAN}settings sound [0 / 1]{colorama.Fore.GREEN} - звук в игре. 0 - отключить, 1 - включить.\n")
                    case 'debug':
                        print(
                            f"{colorama.Fore.CYAN}settings debug [0 / 1]{colorama.Fore.GREEN} - режим отладки (для разработчиков). 0 - отключить, 1 - включить.\n")
                    case _:
                        if components.SETTINGS.sound:
                            playsound3.playsound("base//game//res//audio//invalid_argument.mp3", False)
                        print(
                            f"{colorama.Fore.RED}Неизвестный аргумент команды. Введите {colorama.Fore.CYAN}settings{colorama.Fore.RED}, если понадобится помощь.")
            else:
                t = (
                    f"{colorama.Fore.GREEN}Настройки игры:\n"
                    f"Планеты сообщества: {colorama.Fore.CYAN}{'включены' if components.SETTINGS.get_custom_planets_support() else 'отключены'}{colorama.Fore.GREEN}\n\n"
                    f"Язык: {colorama.Fore.CYAN}{get_lang_name(components.SETTINGS.get_lang())}{colorama.Fore.GREEN}\n"
                    f"Звуки: {colorama.Fore.CYAN}{'включены' if components.SETTINGS.get_sound() else 'отключены'}{colorama.Fore.GREEN}\n\n"
                    f"Отладка: {colorama.Fore.CYAN}{'включена' if components.SETTINGS.get_debug_mode() else 'отключена'}{colorama.Fore.GREEN}\n\n"
                    f"Доступные языки: {colorama.Fore.CYAN}ru{colorama.Fore.GREEN}\n\n"
                    "Изменение настроек:\n"
                    f"{colorama.Fore.CYAN}settings community [0 / 1]{colorama.Fore.GREEN} - планеты сообщества. 0 - отключить, 1 - включить.\n"
                    f"{colorama.Fore.CYAN}settings lang [код]{colorama.Fore.GREEN} - смена языка по коду, которые вы увидите выше.\n"
                    f"{colorama.Fore.CYAN}settings sound [0 / 1]{colorama.Fore.GREEN} - звук в игре. 0 - отключить, 1 - включить.\n"
                    f"{colorama.Fore.CYAN}settings debug [0 / 1]{colorama.Fore.GREEN} - режим отладки (для разработчиков). 0 - отключить, 1 - включить.\n"
                )
                print(t)
                del t

        # Если игрок ничего не ввёл, обрабатывать ввод не нужно.
        if len(command) < 1:
            del command
            return self

        match command[0]:
            case "start":
                if components.SETTINGS.get_debug_mode():
                    print("Ожидается запуск игры")
                return init_game_launch(components.SETTINGS.get_debug_mode())
            case "info":
                a = (
                    f"{colorama.Fore.CYAN}{PRODUCT_NAME}{colorama.Fore.GREEN} - игра про космос на Python, которая разрабатывается в свободное время небольшой командой разработчиков.\n\n"
                    f"{colorama.Fore.CYAN}@pxffd{colorama.Fore.GREEN} - Автор идеи и главный разработчик\n"
                    f"{colorama.Fore.CYAN}неизвестный фанат{colorama.Fore.GREEN} - Автор обложки игры.\n\n"
                    f"{colorama.Fore.CYAN}{PRODUCT_GITHUB_LINK}{colorama.Fore.GREEN} - Исходный код игры и обратная связь.\n"
                )
                print(a)
                del a
            case "settings":
                handle_settings_command(command)
            case "exit":
                if components.SETTINGS.get_sound():
                    playsound3.playsound("base//game//res//audio//shutting_down_basic_systems.mp3", False)
                if components.SETTINGS.get_debug_mode():
                    print("Ожидается выход из игры")
                slow_print("Отключение базовых систем......", colorama.Fore.GREEN, 0.082)
                components.ENGINE.stop()
            # Игрок ввёл неизвестную команду
            case _:
                if components.SETTINGS.sound:
                    playsound3.playsound("base//game//res//audio//unknown_command.mp3", False)
                print(colorama.Fore.RED + "Неизвестная команда.")
        del command
        return self

    def update(self):
        pass
