from src.api.window import Window
from src.api.screen import MainScreen


if __name__ == '__main__':
    window = Window()

    window.show()

    screen = window.detect_screen()

    if type(screen) == MainScreen:
        screen.collect_resources()

    window.hide()