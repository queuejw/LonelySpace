from base.core.constants import DEBUG_MODE


async def init_game():
    from base.core import components
    await components.ENGINE.start()


if __name__ == "__main__":
    import asyncio
    import colorama

    colorama.init(autoreset=True)
    try:
        asyncio.run(init_game())
        if DEBUG_MODE:
            print("Выполнение программы завершено. До скорой встречи!")
    except KeyboardInterrupt:
        print(f"{colorama.Back.RED}{colorama.Fore.BLACK}Экстренное завершение работы системы ...")
    except Exception as e:
        print(
            f"{colorama.Back.RED}{colorama.Fore.BLACK}Возникла критическая ошибка. Игру необходимо перезапустить.{colorama.Style.RESET_ALL}\n\n{colorama.Fore.RED}Информация для разработчиков:\n{e}")
