import time

# Приостанавливает выполнение программы на n секунд.
pause = lambda n: time.sleep(n)


# Возвращает число в пределах лимитов min и max.
def clamp(x, min_value, max_value):
    return max(min_value, min(x, max_value))
