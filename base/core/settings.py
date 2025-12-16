# Класс, который содержит настройки игры.
class Settings:
    def __init__(self):
        self.custom_planets = True
        self.lang = 'ru'
        self.sound = True
        self.debug_mode = False

    def get_custom_planets_support(self) -> bool:
        return self.custom_planets

    def get_lang(self) -> str:
        return self.lang

    def get_sound(self) -> bool:
        return self.sound

    def get_debug_mode(self) -> bool:
        return self.debug_mode

    def export_as_dict(self) -> dict:
        return {
            'custom_planets': self.custom_planets,
            'lang': self.lang,
            'sound': self.sound,
            'debug_mode': self.debug_mode
        }
