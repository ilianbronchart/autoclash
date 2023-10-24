import cv2
import numpy as np

def detect_button(screenshot, template):
    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Get dimensions of the template
    h, w = template_gray.shape
    
    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    
    # Set a threshold value to consider a match
    threshold = 0.1
    print(result)
    loc = np.where(result >= threshold)
    
    # If no match is found, return None
    if len(loc[0]) == 0:
        return None

    # Get the location of the first match
    for pt in zip(*loc[::-1]):
        return (pt[0], pt[1], w, h)