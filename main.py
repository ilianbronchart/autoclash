from src.api.current_screen import find_and_screenshot_window, recognize_game_screen, recognize_game_screen_opencv, detect_text
from src.config import WINDOW_TITLE

if __name__ == '__main__':
  screenshot_np = find_and_screenshot_window(WINDOW_TITLE)
  screen = recognize_game_screen_opencv(screenshot_np)
  print(screen)
  print(detect_text(screenshot_np))