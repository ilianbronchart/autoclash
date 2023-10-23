from src.api.current_screen import find_and_screenshot_window, compile_text_samples, detect_text_thresholded, detect_screen
from src.config import WINDOW_TITLE, OCR_SAMPLES, SCREEN_TEXT

if __name__ == '__main__':
    screenshots = find_and_screenshot_window(WINDOW_TITLE, OCR_SAMPLES)

    words = compile_text_samples(screenshots)
    print(words)
    
    print()

    screen = detect_screen(words)
    print(screen)
