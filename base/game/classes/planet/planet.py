from base.game.classes.base.game_event import GameEvent


class Planet:
    """
    Класс планеты

    Записка от пришельцев, типы планет:
        0	Газовый гигант
        1	Каменистая
        2	Ледяная
        3	Вулканическая
        4	Океаническая
        5	Пустынная
        6	Токсичная
    """

    def __init__(self, m_id: int, m_name: str, m_description: str, m_type: int, m_danger: int, m_eta: int, m_temp: int,
                 m_events: list[GameEvent], m_custom_planet: bool, m_author: str):
        self.planet_id: int = m_id  # Id планеты
        self.planet_name: str = m_name  # Название планеты
        self.planet_description: str = m_description  # Описание планеты
        self.planet_type: int = m_type  # Тип планеты
        self.planet_danger: int = m_danger  # Уровень опасности (от 0 до 9)
        self.planet_eta: int = m_eta  # Примерное время полёта
        self.planet_temp: int = m_temp  # Средняя температура на планете
        self.planet_events: list[
            GameEvent] = m_events  # События, которые могут произойти на планете. Подробнее в database/CREATING-PLANETS.md
        self.custom_planet: bool = m_custom_planet  # Это планета сообщества?
        self.planet_author: str = m_author  # Автор планеты

    # Возвращает текст типа планеты
    def get_planet_type_name(self) -> str:
        match self.planet_type:
            case 0:
                return 'Газовый гигант'
            case 1:
                return 'Каменистая'
            case 2:
                return 'Ледяная'
            case 3:
                return 'Вулканическая'
            case 4:
                return 'Океаническая'
            case 5:
                return 'Пустынная'
            case 6:
                return 'Токсичная'
            case _:
                return 'Неизвестно'
