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

    from base.core.io import json_manager
    from base.core.constants import SETTINGS_FILE_PATH
    from base.core.settings import Settings
    loaded_settings = json_manager.load_file(SETTINGS_FILE_PATH, True)
    components.SETTINGS = Settings(loaded_settings['lang'], loaded_settings['sound'] if check_sound_support() else False, loaded_settings['debug_mode'])
    del loaded_settings

# Запускает движок игры
async def init_game():
    create_game_settings()
    await components.ENGINE.start()

# Здесь происходит запуск программы 
if __name__ == "__main__":
    import asyncio
    import colorama

    colorama.init(autoreset=True)
    try:
        asyncio.run(init_game())
    except KeyboardInterrupt:
        print(f"{colorama.Back.RED}{colorama.Fore.BLACK}Экстренное завершение работы системы ...")
    except Exception as e:
        print(
            f"{colorama.Back.RED}{colorama.Fore.BLACK}Возникла критическая ошибка. Игру необходимо перезапустить.{colorama.Style.RESET_ALL}\n\n{colorama.Fore.RED}Информация для разработчиков:\n{e}")