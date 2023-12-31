from typing import List
import cv2
import numpy as np
from src.config import REFERENCE_SCREEN_SIZE


def click_event(event, x, y, flags, params):
    # Retrieve the image from the params
    img = params["img"]

    # Check for left mouse click event
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the color of the pixel at the clicked coordinates
        # The returned color will be in BGR format
        color = img[y, x]
        # Convert the color to RGB format
        color = (color[2], color[1], color[0])
        print("Color at position (", x, ",", y, "):", color)


def show_image(img):
    window_name = "Image"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img)
    cv2.setMouseCallback(window_name, click_event, {"img": img})
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    cv2.setWindowProperty(
        window_name, cv2.WND_PROP_TOPMOST, 0
    )  # Not always necessary, but can help in some environments

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key != 255:
            break

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
