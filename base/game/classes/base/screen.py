import colorama


class ScreenBase:

    def __init__(self):
        self.name = "placeholder"

    def render(self):
        print(colorama.Fore.RED + "This screen not implemented")

    def handle_input(self, command: str):
        print(colorama.Fore.RED + "Input method for this screen not implemented")
        return self

    def update(self):
        print(colorama.Fore.YELLOW + "\rUpdate method for this screen not yet implemented")
