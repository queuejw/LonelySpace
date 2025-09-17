# Режим отладки, только для разработчиков.
DEBUG_MODE_ENABLED = False

# Название файла конфигурации.
DEFAULT_CONFIG_NAME = "game_config.json"

# Содержимое конфигурации игры.
DEFAULT_GAME_CONFIG = {
    'difficulty': 0,  # Сложность игры. 0 - Нормальная; 1 - Тяжёлая;
    'lang': 'en'  # Язык. Доступные варианты: en ; ru
}

# Название файла сохранения, содержимое генерируется динамически в зависимости от версии.
DEFAULT_SAVE_NAME = "save.json"

### Константы игры
SHIP_LVL_0_SPEED = 1250
SHIP_LVL_1_SPEED = 2500
SHIP_LVL_2_SPEED = 4200
SHIP_LVL_3_SPEED = 5000
