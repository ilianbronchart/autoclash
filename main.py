from src.api.current_screen import screenshot_window, compile_text_samples, detect_text_thresholded, detect_screen, get_window
from src.config import OCR_SAMPLES
from src.utils import show_image

if __name__ == '__main__':
    window = get_window()
    screenshots = screenshot_window(window, OCR_SAMPLES)

    show_image(screenshots[-1])

    # detect_text_thresholded(screenshots[0], True)

    # words = compile_text_samples(screenshots)
    # print(words)
    
    # print()

    # screen = detect_screen(words)
    # print(screen)
