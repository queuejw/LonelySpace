from core.console_manager import print_colored_text

print("Загрузка ...")

from colorama import \
    just_fix_windows_console, Back, \
    Fore  # Исправление консоли в Windows для работы цветного вывода (из библиотеки colorama)

from core.menus import main_menu

if __name__ == '__main__':
    just_fix_windows_console()  # Функция библиотеки colorama
    try:
        main_menu.run_main_menu()  # Запуск главного меню, из которого выполняется вся остальная работа
    except KeyboardInterrupt:
        print_colored_text(Fore.BLACK +"Работы игры была завершена неправильно. Данные могут быть повреждены.",
                           Back.RED)
        exit(0)
