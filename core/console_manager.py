from time import sleep

from colorama import Fore


# Функция, которая выводит цветной текст при помощи библиотеки colorama (по умолчанию - зеленый)
def print_colored_text(text: str, color: str = Fore.GREEN):
    print(color + text)


# Функция, которая медленно выводит текст (по символам)
def slow_print_colored_text(text: str, delay: float = 0.1, color: str = Fore.GREEN):
    text = color + text
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)


# Функция, которая *очищает* окно с небольшой анимацией загрузки.
def clear_terminal():
    slow_print_colored_text("======")
    print("\n" * 100)
