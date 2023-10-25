from src.api.window import Window
from src.api.screen import MainScreen, AttackScreen



if __name__ == '__main__':
    # Create an instance of Window with the AttackScreen
    window = Window()

    # Show the game window
    window.show()

    # Navigate to the attack screen in the game manually

    # Detect the current screen
    current_screen = window.detect_screen()
    if current_screen.name != 'attack_screen':
        print("Please navigate to the attack screen and try again.")
    else:
        print("Attack screen detected!")

        # Take a screenshot
        screenshot = window.screenshot()

        # Detect buttons on the screen
        current_screen.detect_buttons()

        # Perform actions
        current_screen.next_attack(times=3)
        current_screen.end_battle()

        # Hide the game window (optional)
        window.hide()
