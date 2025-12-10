# Используется для загрузки рисунка корабля из txt файла.
def load_txt_file(path: str) -> str:
    f = open(path)
    result = f.read()
    f.close()
    return result
