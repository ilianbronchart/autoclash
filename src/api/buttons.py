import cv2
import numpy as np
import os
from src.config import SCREENS, TEMPLATES_DIR, REFERENCE_SCREEN_SIZE

def detect_button(screenshot, template):
    assert (
        screenshot.shape[0] == REFERENCE_SCREEN_SIZE[1] and 
        screenshot.shape[1] == REFERENCE_SCREEN_SIZE[0]
    ), f'screenshot should have shape {REFERENCE_SCREEN_SIZE}'

    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Get dimensions of the template
    h, w = template_gray.shape
    
    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    
    # Set a threshold value to consider a match
    threshold = 0.8
    loc = np.where(result >= threshold)
    
    # If no match is found, return None
    if len(loc[0]) == 0:
        return None

    # Get the location of the first match
    for pt in zip(*loc[::-1]):
        return (pt[0], pt[1], w, h)
    
def detect_buttons(screenshot, templates):
    assert (
        screenshot.shape[0] == REFERENCE_SCREEN_SIZE[1] and 
        screenshot.shape[1] == REFERENCE_SCREEN_SIZE[0]
    ), f'screenshot should have shape {REFERENCE_SCREEN_SIZE}'
    
    return {template: detect_button(screenshot, templates[template]) for template in templates}

def get_button_templates(screen):
    buttons = SCREENS[screen]['buttons']
    templates = {}

    for button in buttons:
        template = cv2.imread(os.path.join(TEMPLATES_DIR, f"{button}.png"))
        templates[button] = template

    return templates