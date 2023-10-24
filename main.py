from src.api.current_screen import screenshot_window, detect_screen, get_window
from src.api.buttons import detect_button
from src.config import OCR_SAMPLES
from src.utils import show_image
import cv2

if __name__ == '__main__':
    window = get_window()
    screen = detect_screen(window, OCR_SAMPLES)
    print(screen)

    screenshot = screenshot_window(window)[0]
    template = cv2.imread('assets/templates/attack_button.png')
    attack_button = detect_button(screenshot, template)
    print(attack_button)

    x, y, w, h = attack_button
    # Draw a rectangle around the detected button
    cv2.rectangle(screenshot, (x, y), (x+w, y+h), (0, 255, 0), 2)
    show_image(screenshot)