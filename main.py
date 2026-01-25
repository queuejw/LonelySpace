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
            if check_sound_support():
                components.SETTINGS.sound = loaded_settings['sound']
            else:
                components.SETTINGS.sound = False
        except KeyError:
            components.SETTINGS.sound = False
            if components.SETTINGS.get_debug_mode():
                print(f"{colorama.Fore.RED}Не удалось загрузить значение настройки sound")
        try:
            components.SETTINGS.lang = loaded_settings['lang']
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

# Здесь происходит запуск программы 
if __name__ == "__main__":
    import asyncio

    try:
        import colorama
    except ImportError:
        print("[E] Отсутствуют необходимые библиотеки. Обратитесь к документации, чтобы исправить это.")
        exit(1)

    colorama.init(autoreset=True)
    try:
        asyncio.run(init_game())
    except KeyboardInterrupt:
        print(f"{colorama.Back.RED}{colorama.Fore.BLACK}Экстренное завершение работы системы ...")
    except Exception as e:
        print(
            f"{colorama.Back.RED}{colorama.Fore.BLACK}Возникла критическая ошибка. Игру необходимо перезапустить.{colorama.Style.RESET_ALL}\n\n{colorama.Fore.RED}Информация для разработчиков:\n{e}")