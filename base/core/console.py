import os
import time


# Очищает терминал
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# Посимвольно выводит текст на экран
def slow_print(text: str, color: str, sleep_time: float = 0.04):
    for c in text:
        print(color + c, end='', flush=True)
        time.sleep(sleep_time)
    print()
