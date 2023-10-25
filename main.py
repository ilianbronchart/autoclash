from src.api.window import Window
from src.api.screen import MainScreen, AttackScreen


if __name__ == '__main__':
    window = Window()

    window.show()

    screen = window.detect_screen()

    if type(screen) == MainScreen:
        screen.collect_resources()

    if type(screen) == AttackScreen:
        screen.detect_buttons()

    window.hide()