import cv2
import numpy as np
from src.utils import show_image


def extract_white_text(img, lo=190, hi=255):
    original = img.copy()

    # Define a color threshold close to white
    lower_white = np.array([lo, lo, lo], dtype="uint8")
    upper_white = np.array([hi, hi, hi], dtype="uint8")

    # Apply the threshold to get only near white colors
    mask = filter_components(cv2.inRange(img, lower_white, upper_white))

    # Resize the image to make the text bigger
    original = cv2.resize(original, (original.shape[1] * 5, original.shape[0] * 5))
    img = cv2.resize(img, (img.shape[1] * 5, img.shape[0] * 5))
    mask = cv2.resize(mask, (mask.shape[1] * 5, mask.shape[0] * 5))

    show_image(mask)
    img = cv2.bitwise_and(img, img, mask=mask)

    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert to 1-bit mask
    _, mask = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)

    # Dilate the mask to cover more than the text
    kernel = np.ones((5, 5), np.uint8)
    mask_dilated = cv2.dilate(mask, kernel, iterations=2)

    # Apply the dilated mask onto the resized original image
    img_guided = cv2.bitwise_and(original, original, mask=mask_dilated)
    show_image(img_guided)

    # Resize back to original dimensions if needed
    img_guided = cv2.resize(
        img_guided, (img_guided.shape[1] // 5, img_guided.shape[0] // 5)
    )

    # Convert back to RGB format
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    return img_guided


def filter_components(mask, max_size=1000):
    nb_components, output, stats, _ = cv2.connectedComponentsWithStats(
        mask, connectivity=8
    )
    sizes = stats[1:, -1]

    mask = np.zeros(output.shape, dtype=np.uint8)
    for i in range(1, nb_components):
        if sizes[i - 1] < max_size:
            mask[output == i] = 255

    return mask
