print("Загрузка ...")

from colorama import \
    just_fix_windows_console  # Исправление консоли в Windows для работы цветного вывода (из библиотеки colorama)

from core.menus import main_menu

if __name__ == '__main__':
    just_fix_windows_console()  # Функция библиотеки colorama   
    main_menu.run_main_menu()  # Запуск главного меню.
