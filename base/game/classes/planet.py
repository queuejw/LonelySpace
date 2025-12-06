class Planet:
    """
    Записка от пришельцев, типы планет:
        0	Газовый гигант
        1	Каменистая
        2	Ледяная
        3	Вулканическая
        4	Океаническая
        5	Пустынная
        6	Токсическая
    """

    def __init__(self, m_id: int, m_name: str, m_description: str, m_type: int, m_danger: int, m_eta: int, m_temp: int):
        self.planet_id = m_id  # Id планеты
        self.planet_name = m_name  # Название планеты
        self.planet_description = m_description  # Описание планеты
        self.planet_type = m_type  # Тип планеты
        self.planet_danger = m_danger  # Уровень опасности (от 0 до 9)
        self.planet_eta = m_eta  # Примерное время полёта
        self.planet_temp = m_temp

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
                return 'Токсическая'
            case _:
                return 'Неизвестно'
