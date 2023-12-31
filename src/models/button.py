import pyautogui as pag
import pygetwindow as gw
import cv2
import numpy as np
from typing import Tuple
import os
from src.config import TEMPLATES_DIR
from src.models.base import Rect
from src.utils import rescale_template


class Button:
    name: str
    rect: Rect

    def click(self, window):
        assert self.is_visible(), f"Button {self.name} is not visible"

        pag.moveTo(
            window.rect.x + self.rect.center.x, window.rect.y + self.rect.center.y
        )
        pag.click()

    def is_visible(self):
        return self.rect != Rect.zero()


class TemplateButton(Button):
    def __init__(self, name: str, rect: Rect = Rect.zero()):
        self.name = name
        self.rect = rect
        self.template = cv2.imread(os.path.join(TEMPLATES_DIR, f"{self.name}.png"))

    def detect(self, screenshot):
        # Convert screenshot to grayscale
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Convert template to grayscale and get alpha channel
        template_bgr = self.template[:, :, :3]
        template_gray = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2GRAY)
        alpha_channel = self.template[:, :, 3]

        # Set the pixels in the screenshot to a constant value where the template is transparent
        mask = alpha_channel == 0
        template_gray[
            mask
        ] = 128  # Set to mid-gray, you might need to adjust this value
        screenshot_gray[
            mask
        ] = 128  # Set to mid-gray, you might need to adjust this value

        # Rescale the template based on the screenshot size
        target_screenshot_size = (
            screenshot.shape[1],
            screenshot.shape[0],
        )  # Shape returns (height, width), so we reverse it
        rescaled_template = rescale_template(template_gray, target_screenshot_size)

        # Get dimensions of the rescaled template
        h, w = rescaled_template.shape

        # Perform template matching
        result = cv2.matchTemplate(
            screenshot_gray, rescaled_template, cv2.TM_CCOEFF_NORMED
        )

        # Set a threshold value to consider a match
        threshold = 0.7
        loc = np.where(result >= threshold)

        # If no match is found, return None
        if len(loc[0]) == 0:
            self.rect = Rect.zero()

        # Get the location of the first match
        for pt in zip(*loc[::-1]):
            self.rect = Rect(x=pt[0], y=pt[1], w=w, h=h)
            return


class TextButton(Button):
    def __init__(self, name: str, rect: Rect = Rect.zero()):
        self.name = name
        self.rect = rect
