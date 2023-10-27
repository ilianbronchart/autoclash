import cv2
import numpy as np


def extract_white_text(img, contrast=2.0, brightness=50, lo=230, hi=255):
    # Define a color threshold close to white
    lower_white = np.array([lo, lo, lo], dtype="uint8")
    upper_white = np.array([hi, hi, hi], dtype="uint8")

    # Apply the threshold to get only near white colors
    mask = cv2.inRange(img, lower_white, upper_white)
    img = cv2.bitwise_and(img, img, mask=mask)

    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Define a kernel for erosion and dilation
    kernel = np.ones((2, 2), np.uint8)

    # Erode to remove noise
    img = cv2.erode(img, kernel, iterations=1)

    # Dilate to restore the shape
    img = cv2.dilate(img, kernel, iterations=1)

    # Convert to 1-bit mask
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)

    # Convert back to RGB format
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    return img
