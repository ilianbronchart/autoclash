import cv2
from src.utils import show_image


def useful_preprocessing_steps(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert the image
    invert = cv2.bitwise_not(gray)

    # Apply thresholding to get a binary image
    thresh = cv2.threshold(invert, 25, 255, cv2.THRESH_BINARY)[1]

    # Resize
    thresh = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    show_image(thresh)


def find_connected_components(img):
    pass
