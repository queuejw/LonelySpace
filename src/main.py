from base.core import components


# Загружает настройки игры
def create_game_settings():

    # Если звук недоступен, вернет False
    def check_sound_support() -> bool:
        from playsound3 import AVAILABLE_BACKENDS
        if len(AVAILABLE_BACKENDS) < 1:
            print(f"{colorama.Fore.RED}Не удалось включить поддержку звука на Вашей системе.\n\nОбратитесь к справке, либо попробуйте разобраться с этим самостоятельно.")
            input("Нажмите Enter, чтобы продолжить запуск игры.")
            return False
        return True

    def apply_loaded_settings(loaded_settings: dict):
        try:
            components.SETTINGS.debug_mode = loaded_settings['debug_mode']
        except KeyError:
            pass
        try:
            components.SETTINGS.custom_planets = loaded_settings['custom_planets']
        except KeyError:
            if components.SETTINGS.get_debug_mode():
                print(f"{colorama.Fore.RED}Не удалось загрузить значение настройки custom_planets")
        try:
            if not check_sound_support():
                components.SETTINGS.sound = loaded_settings['sound']
            else:
                components.SETTINGS.sound = False
        except KeyError:
            components.SETTINGS.sound = False
            if components.SETTINGS.get_debug_mode():
                print(f"{colorama.Fore.RED}Не удалось загрузить значение настройки sound")
        try:
            components.SETTINGS.sound = loaded_settings['lang']
        except KeyError:
            if components.SETTINGS.get_debug_mode():
                print(f"{colorama.Fore.RED}Не удалось загрузить значение настройки lang")

        del loaded_settings

    from base.core.io import json_manager
    from base.core.constants import SETTINGS_FILE_PATH
    from base.core.settings import Settings
    components.SETTINGS = Settings()
    apply_loaded_settings(json_manager.load_file(SETTINGS_FILE_PATH, True))

# Запускает движок игры
async def init_game():
    create_game_settings()
    await components.ENGINE.start()

# Запускает новую версию игры
# Старя версия будет поддерживаться до тех пор, пока не будет готова версия 2.0.
# Но, стоит учитывать, что по умолчанию запускается старая версия, а не новая. Вот так.
# Файлы новой версии находятся в директории res (не base)
def init_game_v2():
    print("запус")

# Здесь происходит запуск программы 
if __name__ == "__main__":
    import asyncio
    import colorama
    import sys
    args = sys.argv
    colorama.init(autoreset=True)
    try:
        if len(args) > 1:
            # Если есть аргумент new, запускаем новую версию игры (которая на pygame будет)
            if args[1] == "new":
                init_game_v2()
        else:
            asyncio.run(init_game())
    except KeyboardInterrupt:
        print(f"{colorama.Back.RED}{colorama.Fore.BLACK}Экстренное завершение работы системы ...")
    except Exception as e:
        print(
            f"{colorama.Back.RED}{colorama.Fore.BLACK}Возникла критическая ошибка. Игру необходимо перезапустить.{colorama.Style.RESET_ALL}\n\n{colorama.Fore.RED}Информация для разработчиков:\n{e}")