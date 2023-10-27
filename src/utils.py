from typing import List
import cv2
import numpy as np
from src.config import REFERENCE_SCREEN_SIZE, OCR_WHITE_THRESHOLD


def show_image(img):
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def rescale_template(template, target_screenshot_size):
    # Calculate scaling factors for both dimensions
    scale_width = target_screenshot_size[0] / REFERENCE_SCREEN_SIZE[0]
    scale_height = target_screenshot_size[1] / REFERENCE_SCREEN_SIZE[1]

    # Choose the larger scaling factor to ensure the template fits within the screenshot
    # while preserving its aspect ratio
    scale = min(scale_width, scale_height)

    # Compute the new dimensions for the template
    new_width = int(template.shape[1] * scale)
    new_height = int(template.shape[0] * scale)

    # Rescale the template
    rescaled_template = cv2.resize(
        template, (new_width, new_height), interpolation=cv2.INTER_LINEAR
    )

    return rescaled_template


def filter_small_components(binary_img, min_area=50):
    """
    Remove small connected components from a binary image based on a given area threshold.
    """
    # Find all connected components
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        binary_img, connectivity=8
    )

    # Create an output image, initialized as all zeros (black)
    output = np.zeros_like(binary_img)

    # Loop through all connected component labels
    for i in range(1, num_labels):
        # If the area of the connected component is above the threshold, add it to the output image
        if stats[i, cv2.CC_STAT_AREA] > min_area:
            output[labels == i] = 255

    return output


def draw_rects(img, rects):
    img = img.copy()
    for x, y, w, h in rects:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)

    show_image(img)
