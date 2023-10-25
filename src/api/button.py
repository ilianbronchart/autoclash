import pyautogui as pag
import pygetwindow as gw
import cv2
import numpy as np
from typing import Tuple
import os
from src.config import TEMPLATES_DIR
from src.utils import rescale_template


class Button:
    def __init__(self, name: str, rect: Tuple[int, int, int, int] = (0, 0, 0, 0)):
        self.name = name
        self.rect = rect
        self.template = cv2.imread(os.path.join(TEMPLATES_DIR, f"{self.name}.png"))


    def click(self, window):
        center_x = window.left + self.rect[0] + self.rect[2] // 2
        center_y = window.top + self.rect[1] + self.rect[3] // 2
        pag.moveTo(center_x, center_y)
        pag.click()


    def detect(self, screenshot):
        # Convert images to grayscale
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)

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
            self.rect = (pt[0], pt[1], w, h)
            return