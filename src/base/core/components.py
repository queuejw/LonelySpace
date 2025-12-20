from base.core.settings import Settings
from base.game.classes.engine import Engine
from base.game.classes.game import Game

# Связующее звено между элементами игры
SETTINGS: Settings  # Настройки игры
ENGINE = Engine()  # Движок
GAME: Game  # Игра
