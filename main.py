from src.api.current_screen import find_and_screenshot_window, recognize_game_screen
from src.config import WINDOW_TITLE

if __name__ == '__main__':
  screenshot_np = find_and_screenshot_window(WINDOW_TITLE)
  recognize_game_screen(screenshot_np)
