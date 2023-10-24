from src.api.current_screen import screenshot_window, detect_screen, get_window, compile_text_samples
from src.api.buttons import detect_buttons, get_button_templates
from src.config import OCR_SAMPLES, REFERENCE_SCREEN_SIZE
from src.utils import show_image, show_button_rects, show_window


if __name__ == '__main__':
    window = get_window()
    show_window(window)

    # screen = detect_screen(window, OCR_SAMPLES)
    # print(screen)

    screen = 'main_screen'

    screenshot = screenshot_window(window, 1, 'assets')[0]
    templates = get_button_templates(screen)
    buttons = detect_buttons(window, screenshot, templates)

    window.minimize()

    show_button_rects(screenshot, buttons)