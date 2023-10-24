import cv2
import numpy as np
import os
import pyautogui as pag
from src.config import SCREENS, TEMPLATES_DIR, REFERENCE_SCREEN_SIZE, TEMPLATE_TO_COLOR
from src.api.models import Button
from src.utils import show_image


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
    rescaled_template = cv2.resize(template, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    return rescaled_template

def detect_button_gray(screenshot, template):
    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Rescale the template based on the screenshot size
    target_screenshot_size = (screenshot.shape[1], screenshot.shape[0])  # Shape returns (height, width), so we reverse it
    rescaled_template = rescale_template(template_gray, target_screenshot_size)
    
    # Get dimensions of the rescaled template
    h, w = rescaled_template.shape
    
    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, rescaled_template, cv2.TM_CCOEFF_NORMED)
    
    # Set a threshold value to consider a match
    threshold = 0.7
    loc = np.where(result >= threshold)
    
    # If no match is found, return None
    if len(loc[0]) == 0:
        return None

    # Get the location of the first match
    for pt in zip(*loc[::-1]):
        return (pt[0], pt[1], w, h)


def detect_button_color(screenshot, template): 
    # Rescale the template based on the screenshot size
    target_screenshot_size = (screenshot.shape[1], screenshot.shape[0])  # Shape returns (height, width), so we reverse it
    rescaled_template = rescale_template(template, target_screenshot_size)
    
    # Get dimensions of the rescaled template
    h, w = rescaled_template.shape[:2]
    
    # Perform template matching
    result = cv2.matchTemplate(screenshot, rescaled_template, cv2.TM_CCOEFF_NORMED)
    
    # Set a threshold value to consider a match
    threshold = 0.7
    loc = np.where(result >= threshold)
    
    # If no match is found, return None
    if len(loc[0]) == 0:
        return None

    # Get the location of the first match
    for pt in zip(*loc[::-1]):
        return (pt[0], pt[1], w, h)

    
def detect_buttons(window, screenshot, templates):
    buttons = {}

    for template in templates:
        if template in TEMPLATE_TO_COLOR:
            rect = detect_button_color(screenshot, templates[template])
        else:
            rect = detect_button_gray(screenshot, templates[template])

        print(template, rect)
        if (rect):
            buttons[template] = Button(window, rect)

    return buttons


def get_button_templates(screen):
    buttons = SCREENS[screen]['buttons']
    templates = {}

    for button in buttons:
        template = cv2.imread(os.path.join(TEMPLATES_DIR, f"{button}.png"))
        templates[button] = template

    return templates

