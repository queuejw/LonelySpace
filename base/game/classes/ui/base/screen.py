import colorama

from base.core.constants import DEBUG_MODE


class ScreenBase:

    def __init__(self):
        pass

    def render(self):
        if DEBUG_MODE:
            print(colorama.Fore.RED + "This screen not implemented")

    def handle_input(self, command: str):
        if DEBUG_MODE:
            print(colorama.Fore.RED + "Input method for this screen not implemented")
        return self

    def update(self):
        if DEBUG_MODE:
            print(colorama.Fore.YELLOW + "\rUpdate method for this screen not yet implemented")
