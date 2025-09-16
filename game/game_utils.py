import datetime

from game import game_vars


# Вычисляет, нужен ли ремонт, и возвращает результат
def is_repair_needed() -> bool:
    return game_vars.PLAYER.health < 100 or game_vars.PLAYER.oxygen < 100


# Возвращает дату в таком формате: день, месяц, год
def get_today_date() -> str:
    return f"{datetime.date.today().day}/{datetime.date.today().month}/{datetime.date.today().year}"
