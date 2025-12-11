# Класс, который содержит настройки игры.
class Settings:
    def __init__(self, m_lang: str, m_sound: bool, m_debug: bool):
        self.lang = m_lang
        self.sound = m_sound
        self.debug_mode = m_debug

    def get_lang(self) -> str:
        return self.lang

    def get_sound(self) -> bool:
        return self.sound

    def get_debug_mode(self) -> bool:
        return self.debug_mode

    def export_as_dict(self) -> dict:
        return {
            'lang': self.lang,
            'sound': self.sound,
            'debug_mode': self.debug_mode
        }
