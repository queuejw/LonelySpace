from game.classes.ship import PlayerShip
from game.classes.universe import Universe

UNIVERSE: Universe  # Вселенная
PLAYER: PlayerShip  # Игрок

PAUSED = False  # Остановлена ли игра?
GAME_SCREEN = "main"  # Указывает текущий экран игры
UPDATE_REQUIRED = False  # Требуется ли обновление данных на главном экране?

MAIN_GAME_THREAD_RUNNING = False  # Указывает состояние основного потока игры
