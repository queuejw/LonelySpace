import os
import time


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def slow_print(text: str, color: str):
    for c in text:
        print(color + c, end='', flush=True)
        time.sleep(0.04)
    print()
