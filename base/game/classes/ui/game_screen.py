import asyncio
import random

import colorama

from base.core import components
from base.core import constants
from base.core.console import clear_terminal
from base.core.io.json_manager import save_file
from base.game.classes.base.screen import ScreenBase
from base.game.classes.game import print_terminal_help, print_game_help, print_ship_help, print_planets_help


# Если перевод переменной в int успешный, вернёт True
def is_int(value) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


class GameScreen(ScreenBase):

    def __init__(self):
        super().__init__()
        self.name = "game"

    def render(self):
        if not components.ENGINE.pending_input:
            text = components.GAME.generate_main_text()
            clear_terminal()
            print(text)
            del text

    def handle_input(self, command: str):

        command = command.split()

        # Останавливает игру и возвращает главное меню игры
        def stop_game():
            components.GAME.running = False
            from base.game.classes.ui.main_menu import MainMenu
            return MainMenu()

        # Переименовывает корабль игра
        def rename_player_ship(user_command: list[str]):
            if len(user_command) > 1:
                new_name = ''
                user_command.pop(0)
                for i in user_command:
                    new_name += f'{i} '
                if len(new_name) > 15:
                    print(f"{colorama.Fore.RED}Название слишком длинное.")
                    components.GAME.add_audio_to_queue("base//game//res//audio//command_handle_error.mp3")
                elif len(new_name) < 4:
                    print(f"{colorama.Fore.RED}Название слишком короткое.")
                    components.GAME.add_audio_to_queue("base//game//res//audio//command_handle_error.mp3")
                else:
                    components.GAME.player.ship_name = new_name
                    print(
                        f"{colorama.Fore.GREEN}Название корабля изменено на {colorama.Fore.CYAN}{new_name}{colorama.Fore.GREEN}.")
                    components.GAME.add_audio_to_queue("base//game//res//audio//ship_renamed.mp3")
                del new_name
            else:
                components.GAME.add_audio_to_queue("base//game//res//audio//invalid_argument.mp3")
                print(
                    f"{colorama.Fore.RED}Вы не указали новое название для корабля. Введите {colorama.Fore.CYAN}help ship{colorama.Fore.RED}, если понадобится помощь.")

        # Здесь происходит обработка команды полёта.
        def handle_goto_command(user_command: list[str]):
            # Если указан аргумент команды (какой-то)

            # Если игрок не указал id, то выбираем случайный
            if len(user_command) < 2:
                user_command.append(random.choice(
                    [x.planet_id for x in components.GAME.planets if x not in components.GAME.player.visited_planets]))

            # Если игрок ввёл число
            if is_int(user_command[1]):
                # Если игрок не на планете, то он может начать полёт
                if not components.GAME.player.on_planet:
                    planet_id = int(user_command[1])
                    # Если в данный момент корабль не в пути, можем начать полёт
                    if not components.GAME.planet_flying_active:
                        planet_was_changed = False
                        # Если компьютер поврежден, есть шанс, что планета изменится на случайную.
                        if components.GAME.player.module_computer_damaged and random.random() > 0.7:
                            planet_was_changed = True
                            planet_id = random.choice([x.planet_id for x in components.GAME.planets])
                        # Проверяем, был ли игрок на этой планете.
                        if planet_id in components.GAME.player.visited_planets:
                            if len(user_command) > 2:
                                if user_command[2] != "force":
                                    components.GAME.add_audio_to_queue(
                                        "base//game//res//audio//command_handle_error.mp3")
                                    print(
                                        f"{colorama.Fore.YELLOW}Мы уже были на этой планете. Если хотите отправиться ещё раз, добавьте аргумент {colorama.Fore.CYAN}force{colorama.Fore.YELLOW} в конец команды.\n"
                                        f"{colorama.Fore.GREEN}Пример: goto {planet_id} force"
                                    )
                                    del planet_id
                                    return
                            else:
                                components.GAME.add_audio_to_queue(
                                    "base//game//res//audio//command_handle_error.mp3")
                                print(
                                    f"{colorama.Fore.YELLOW}Мы уже были на этой планете. Если хотите отправиться ещё раз, добавьте аргумент {colorama.Fore.CYAN}force{colorama.Fore.YELLOW} в конец команды.\n"
                                    f"{colorama.Fore.GREEN}Пример: goto {planet_id} force"
                                )
                                del planet_id
                                return
                        if len([x.planet_id for x in components.GAME.planets if x.planet_id == planet_id]) < 1:
                            components.GAME.add_audio_to_queue("base//game//res//audio//invalid_argument.mp3")
                            print(
                                f"{colorama.Fore.RED}Неверный ID планеты. Убедитесь, что ID верный. Введите {colorama.Fore.CYAN}help ship{colorama.Fore.RED}, если понадобится помощь.")
                            del planet_id
                            return
                            # Обновляем значений переменных и запускаем цикл полёта.
                        components.GAME.player.planet_id = planet_id
                        planet = components.GAME.get_planet_by_id(planet_id)
                        asyncio.create_task(components.GAME.fly_cycle(planet.planet_eta, False))
                        components.GAME.add_audio_to_queue("base//game//res//audio//route_updated.mp3")
                        if not planet_was_changed:
                            t = f"{colorama.Fore.GREEN}Маршрут обновлён. Летим на планету {colorama.Fore.CYAN}{planet.planet_name}{colorama.Fore.GREEN}."
                        else:
                            t = f"{colorama.Fore.RED}Маршрут обновлён. {colorama.Fore.GREEN}Летим на план{colorama.Fore.RED}ету {colorama.Fore.CYAN}{planet.planet_name}{colorama.Fore.RED}."
                        print(t)
                        components.GAME.update_last_messages(t)
                        del planet_was_changed
                        del t
                        del planet
                        del planet_id
                    else:
                        # Игрок уже в пути, мы не можем начать одновременно два и более полёта.
                        del planet_id
                        components.GAME.add_audio_to_queue(
                            "base//game//res//audio//command_handle_error.mp3")
                        print(
                            f"{colorama.Fore.RED}Корабль уже в пути. Если хотите изменить маршрут, отмените этот полёт. Введите {colorama.Fore.CYAN}help ship{colorama.Fore.RED}, если понадобится помощь.")
                # Игрок уже на планете, сначала нужно покинуть её.
                else:
                    components.GAME.add_audio_to_queue("base//game//res//audio//command_handle_error.mp3")
                    print(
                        f"{colorama.Fore.RED}Прежде чем лететь на другую планету, нужно покинуть текущую.")
            # Отмена полёта
            elif user_command[1] == 'cancel':
                if components.GAME.planet_flying_active:
                    # Отмечаем, что полёт был завершен.
                    # Цикл прервется автоматически.
                    components.GAME.add_audio_to_queue("base//game//res//audio//route_updated.mp3")
                    components.GAME.planet_flying_active = False
                    print(f"{colorama.Fore.YELLOW}Маршрут обновлён. Полёт прерван.")
                else:
                    components.GAME.add_audio_to_queue("base//game//res//audio//command_handle_error.mp3")
                    print(f"{colorama.Fore.RED}Корабль не находится в пути. Невозможно прервать полёт.")
            # Покинуть планету
            elif user_command[1] == 'leave':
                # Покинуть планету
                if components.GAME.player.on_planet:
                    if not components.GAME.planet_flying_active:
                        planet = components.GAME.get_planet_by_id(components.GAME.player.planet_id)
                        asyncio.create_task(components.GAME.fly_cycle(planet.planet_eta, True))
                        components.GAME.add_audio_to_queue("base//game//res//audio//route_updated.mp3")
                        t = f"{colorama.Fore.GREEN}Маршрут обновлён. Покидаем планету {colorama.Fore.CYAN}{planet.planet_name}{colorama.Fore.GREEN}."
                        print(t)
                        components.GAME.update_last_messages(t)
                        del t
                        del planet
                    else:
                        components.GAME.add_audio_to_queue("base//game//res//audio//command_handle_error.mp3")
                        print(
                            f"{colorama.Fore.RED}Корабль уже в пути. Отмените этот полёт, если хотите вернуться на планету. Введите {colorama.Fore.CYAN}help ship{colorama.Fore.RED}, если понадобится помощь.")
                else:
                    components.GAME.add_audio_to_queue("base//game//res//audio//command_handle_error.mp3")
                    print(
                        f"{colorama.Fore.RED}В данный момент корабль не находится на поверхности какой-либо планеты.")
            else:
                components.GAME.add_audio_to_queue("base//game//res//audio//invalid_argument.mp3")
                print(
                    f"{colorama.Fore.RED}Неверный аргумент команды. Введите {colorama.Fore.CYAN}help ship{colorama.Fore.RED}, если понадобится помощь.")

        def print_planet_info(user_command: list[str]):
            if len(user_command) > 1:
                try:
                    pos = int(command[1])
                    print(components.GAME.get_text_planet_list(pos))
                    components.GAME.add_audio_to_queue("base//game//res//audio//command_executed.mp3")
                    del pos
                except ValueError:
                    print(components.GAME.get_text_planet_list(-1))
            else:
                components.GAME.add_audio_to_queue("base//game//res//audio//command_handle_error.mp3")
                print(
                    f"{colorama.Fore.RED}Укажите аргумент команды. Введите {colorama.Fore.CYAN}help planets{colorama.Fore.RED}, если понадобится помощь.")

        # Если игрок ничего не ввёл, обрабатывать ввод не нужно.
        if len(command) < 1:
            del command
            return self

        if components.SETTINGS.get_debug_mode():
            print(f"{colorama.Fore.MAGENTA}Игрок ввёл команду: {command}{colorama.Fore.RESET}")

        # Если бортовой компьютер поврежден, есть шанс, что произойдет сбой.
        if components.GAME.player.module_computer_damaged and random.random() < 0.2:
            print(
                f"{colorama.Fore.RED}[СБОЙ] {colorama.Fore.GREEN}Попробу{colorama.Fore.YELLOW}йте ещё р{colorama.Fore.WHITE}аз.")
            return self

        # Мы не можем выполнять команды, если игра была остановлена.
        if not components.GAME.running:
            if command[0].lower() == 'stop':
                return stop_game()
            else:
                print(
                    f"{colorama.Fore.YELLOW}Игра завершена, введите {colorama.Fore.CYAN}stop{colorama.Fore.YELLOW}, чтобы отключить бортовой компьютер.")
                return self

        # Остановка игры
        if command[0].lower() == 'stop':
            return stop_game()
        # Помощь
        elif command[0].lower() == 'help':
            if len(command) > 1:
                if command[1].lower() == 'game':
                    components.GAME.add_audio_to_queue("base//game//res//audio//command_executed.mp3")
                    print_game_help()
                elif command[1].lower() == 'ship':
                    components.GAME.add_audio_to_queue("base//game//res//audio//command_executed.mp3")
                    print_ship_help()
                elif command[1].lower() == 'planets':
                    components.GAME.add_audio_to_queue("base//game//res//audio//command_executed.mp3")
                    print_planets_help(len(components.GAME.planets) - 1)
                else:
                    components.GAME.add_audio_to_queue("base//game//res//audio//invalid_argument.mp3")
                    print(
                        f"{colorama.Fore.RED}Неизвестный аргумент команды help. Введите {colorama.Fore.CYAN}help{colorama.Fore.RED},чтобы вывести общие инструкции.")
            else:
                print_terminal_help()
        # Сохранить игру
        elif command[0].lower() == 'save':
            components.GAME.add_audio_to_queue("base//game//res//audio//command_executed.mp3")
            if save_file(components.GAME.player.export_as_dict(), constants.SAVE_FILE_PATH,
                         constants.USER_FOLDER_NAME):
                print(f"{colorama.Fore.CYAN}Игра сохранена!")
            else:
                components.GAME.add_audio_to_queue("base//game//res//audio//command_handle_error.mp3")
                print(f"{colorama.Fore.RED}Не получилось сохранить игру.")
        # Переименовать корабль
        elif command[0].lower() == 'rename':
            rename_player_ship(command)
        # Ремонтировать корабль
        elif command[0].lower() == 'repair':
            if len(command) > 1:
                if command[1].lower() == 'run':
                    print(f"{colorama.Fore.CYAN}Запланирован ремонт корабля.")
                    asyncio.create_task(components.GAME.repair_cycle())
                else:
                    components.GAME.add_audio_to_queue("base//game//res//audio//invalid_argument.mp3")
                    print(
                        f"{colorama.Fore.RED}Неизвестный аргумент команды repair. Введите {colorama.Fore.CYAN}help ship{colorama.Fore.RED},чтобы вывести инструкции.")
            else:
                components.GAME.add_audio_to_queue("base//game//res//audio//command_executed.mp3")
                print(
                    f"{colorama.Fore.GREEN}Стоимость ремонта корабля: {colorama.Fore.CYAN}{components.GAME.get_repair_price()}{colorama.Fore.GREEN} ресурсов."
                    f"\nЭто займёт {colorama.Fore.CYAN}{components.GAME.get_repair_time()}{colorama.Fore.GREEN} секунд."
                    f"\nВведите {colorama.Fore.CYAN}repair run{colorama.Fore.GREEN}, чтобы начать ремонт."
                )
        # Статус корабля
        elif command[0].lower() == 'status':
            components.GAME.add_audio_to_queue("base//game//res//audio//command_executed.mp3")
            print(components.GAME.get_ship_status_text())
        # Перемещение корабля по планетам
        elif command[0].lower() == 'goto':
            handle_goto_command(command)
        # Вывести инфо о планете
        elif command[0].lower() == 'planet':
            print_planet_info(command)
        # Закрыть терминал
        elif command[0].lower() == 'exit':
            if components.GAME.is_audio_queue_empty():
                components.GAME.add_audio_to_queue("base//game//res//audio//terminal_off.mp3")
            components.ENGINE.pending_input = False
            self.update(True)

        else:
            components.GAME.add_audio_to_queue("base//game//res//audio//unknown_command.mp3")
            print(
                f"{colorama.Fore.RED}Неизвестная команда. Если возникли трудности, введите команду {colorama.Fore.CYAN}help{colorama.Fore.GREEN}.")
        del command
        return self

    def update(self, force_update: bool = False):
        if components.GAME.pending_update:
            if not components.ENGINE.pending_input or force_update:
                components.GAME.pending_update = False
                self.render()
