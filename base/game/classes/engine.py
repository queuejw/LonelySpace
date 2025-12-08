import asyncio

import colorama
import keyboard

from base.core import components
from base.core.console import clear_terminal
from base.game.classes.game import Game
from base.game.classes.ui.base.screen import ScreenBase
from base.game.classes.ui.main_menu import MainMenu


# Возвращает стандартный экран, который игрок видит при запуске игры.
def get_default_screen() -> ScreenBase:
    return MainMenu()


# Типа движок игры. Отвечает за рендер экранов и ввода игрока
class Engine:

    # Инициализация движка
    def __init__(self):
        self.screen = get_default_screen()  # Текущий экземпляр объекта экрана.
        self.running = True  # Запущен ли движок? Если нет, игра закрывается.
        self.blocked = False  # Заблокировано ли ядро? Блокирует работу циклов движка (просто пропускает итерацию)
        self.pending_input = True  # Ожидается ли ввод игрока. Костыль для нормальной работы терминала. Работает же)

    # Управляет состоянием интерфейса (блокирует его, либо разблокирует)
    def engine_block_control(self):
        self.blocked = (not self.blocked)

    # Запуск движка (и игры)
    async def start(self):
        # Циклы движка
        tick_task = asyncio.create_task(self.ui_loop())
        input_task = asyncio.create_task(self.input_loop())
        # Циклы самой игры
        components.GAME = Game()
        game_task = asyncio.create_task(components.GAME.main_loop())
        from base.core import constants
        components.GAME.update_last_messages(f"Добро пожаловать в {constants.PRODUCT_NAME}!")
        await asyncio.gather(tick_task, input_task, game_task)

    # Функция для остановки движка
    # По факту все циклы завершатся автоматически, если изменить переменную running на False.
    # От нас дальнейших действий не требуется
    def stop(self):
        self.running = False

    # Цикл, в котором происходит обновление экрана.
    async def ui_loop(self):
        self.screen.render()
        while self.running:
            if not self.blocked:
                self.screen.update()
            await asyncio.sleep(0.5)

    # Устанавливает ожидание ввода игрока, если движок не заблокирован.
    def on_space(self) -> bool:
        if self.blocked:
            return False
        if not self.pending_input:
            self.pending_input = True
        return True

    # Цикл, в котором происходит обработка ввода игрока.
    async def input_loop(self):
        keyboard.add_hotkey('space', self.on_space)  # Если игрок нажал пробел, выполнится функция on_space
        while self.running:
            if not self.blocked and self.pending_input:
                command = await asyncio.to_thread(input, f"{colorama.Fore.GREEN}> ")  # Получаем ввод
                if self.blocked:
                    continue
                updated_screen = self.screen.handle_input(
                    command)  # Для обновления экрана эта функция возвращает значение текущего экрана.
                # Если экран был изменен, обновляем его.
                del command
                # Убеждаемся, что новый экран действительно был изменён.
                if updated_screen is not None and updated_screen != self.screen:
                    self.screen = updated_screen
                    clear_terminal()
                    self.screen.render()
            else:
                # Если ожидается ввод, то пропускаем итерацию, просто ждём.
                await asyncio.sleep(0.05)
