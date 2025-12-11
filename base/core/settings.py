# Класс, который содержит настройки игры.
class Settings:
    def __init__(self, m_lang: str, m_sound: bool):
        self.lang = m_lang
        self.sound = m_sound

    def get_lang(self) -> str:
        return self.lang

    def get_sound(self) -> bool:
        return self.sound

    def export_as_dict(self) -> dict:
        return {
            'lang': self.lang,
            'sound': self.sound
        }
