from core.console_manager import print_colored_text
from core.translation_manager import TRANSLATIONS


# Выводит сообщение об неизвестной команде
def menu_unknown_key_code():
    print_colored_text(TRANSLATIONS['input_error'])
