from src.api.window import Window


if __name__ == '__main__':
    window = Window()

    window.show()

    screen = window.detect_screen()
    print(screen.name) 

    window.hide()