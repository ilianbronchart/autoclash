from src.api.window import Window
from src.api.screen import MainScreen, AttackScreen, TrainingScreen


if __name__ == '__main__':
    window = Window()

    window.show()

    # window.screenshot('assets')

    current_screen = window.detect_screen()

    current_screen.detect_buttons()
    current_screen.show_buttons(window.screenshot())

    window.hide()