import cv2

def show_image(img):
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_button_rects(screenshot, buttons):
    for button in buttons.keys():
        x, y, w, h = buttons[button].rect
        cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)

        show_image(screenshot)


def show_window(window):
    try:
        window.activate()
    except:
        pass
    window.restore()
