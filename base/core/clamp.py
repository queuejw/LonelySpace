# Возвращает новое значение в пределах от min_value до max_value
def clamp(value, min_value, max_value):
    if value > max_value:
        return max_value
    if value < min_value:
        return min_value
    return value