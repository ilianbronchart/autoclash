from src.api.current_screen import screenshot_window, detect_screen, get_window, compile_text_samples
from src.api.buttons import detect_buttons, get_button_templates
from src.config import OCR_SAMPLES, REFERENCE_SCREEN_SIZE
from src.utils import show_image
import cv2

if __name__ == '__main__':
    window = get_window()
    screen = detect_screen(window, OCR_SAMPLES)
    print(screen)

    screenshot = screenshot_window(window, 1, 'assets')[0]

    templates = get_button_templates(screen)
    buttons = detect_buttons(screenshot, templates)

    for button in buttons.keys():
        if not button:
            print(f'Could not find {button}')
            continue

        x, y, w, h = buttons[button]
        cv2.rectangle(screenshot, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
    show_image(screenshot)