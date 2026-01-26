# Загружает настройки игры, а затем запускает её
async def start_game_services():
    from base.core import components

    # Если звук на этой системе недоступен, вернет False
    def check_sound_support() -> bool:
        from playsound3 import AVAILABLE_BACKENDS
        if len(AVAILABLE_BACKENDS) < 1:
            print(
                f"{colorama.Fore.RED}Не удалось включить поддержку звука на Вашей системе.\n\nОбратитесь к справке, либо попробуйте разобраться с этим самостоятельно.")
            input("Нажмите Enter, чтобы продолжить запуск игры.")
            return False
        return True

    from base.core.settings import Settings

    # Возвращает настройки игрока
    def load_user_settings() -> Settings:

        from base.core.io import json_manager
        from base.core.constants import SETTINGS_FILE_PATH
        loaded_settings = json_manager.load_file(SETTINGS_FILE_PATH, True)

        game_settings = Settings()
        # Пробуем загрузить значение debug_mode
        try:
            game_settings.debug_mode = loaded_settings['debug_mode']
        except KeyError:
            # Режим отладки недоступен.
            pass
        # Пробуем загрузить значение custom_planets
        try:
            game_settings.custom_planets = loaded_settings['custom_planets']
        except KeyError:
            if game_settings.get_debug_mode():
                print(f"{colorama.Fore.RED}Не удалось загрузить значение настройки custom_planets")
        # Пробуем загрузить значение
        try:
            game_settings.custom_planets = loaded_settings['custom_space_events']
        except KeyError:
            if game_settings.get_debug_mode():
                print(f"{colorama.Fore.RED}Не удалось загрузить значение настройки custom_space_events")
        # Пробуем загрузить значение sound
        try:
            if check_sound_support():
                game_settings.sound = loaded_settings['sound']
            else:
                # Если звук не поддерживается, мы должны отключить его, чтобы избежать проблем
                game_settings.sound = False
        except KeyError:
            game_settings.sound = False
            if game_settings.get_debug_mode():
                print(f"{colorama.Fore.RED}Не удалось загрузить значение настройки sound")
        # Пробуем загрузить значение lang
        try:
            game_settings.lang = loaded_settings['lang']
        except KeyError:
            if game_settings.get_debug_mode():
                print(f"{colorama.Fore.RED}Не удалось загрузить значение настройки lang")

        del loaded_settings
        # Возвращаем загруженные настройки
        return game_settings

    components.SETTINGS = load_user_settings()

    await components.ENGINE.start()

# Здесь происходит запуск программы
if __name__ == "__main__":

    # Импортируем все библиотеки, чтобы проверить их наличие. В случае ошибки игра закроется
    try:
        import colorama
        import playsound3
        import keyboard
    except ImportError:
        print("[E] Отсутствуют необходимые библиотеки. Обратитесь к документации, чтобы исправить это.")
        exit(1)
    # Инициализация colorama
    colorama.init(autoreset=True)
    import asyncio

    # Запускаем игру?
    try:
        asyncio.run(start_game_services())
    except KeyboardInterrupt:
        print(f"{colorama.Back.RED}{colorama.Fore.BLACK}Экстренное завершение работы системы ...")
    except Exception as e:
        print(
            f"{colorama.Back.RED}{colorama.Fore.BLACK}Возникла критическая ошибка. Игру необходимо перезапустить.{colorama.Style.RESET_ALL}\n\n{colorama.Fore.RED}Информация для разработчиков:\n{e}")
