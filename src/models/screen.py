import cv2
import re
import pyautogui as pag
from typing import List
from src.models.button import Button
from src.utils import show_image
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.window import Window


class Screen:
    words: List[str]
    window: "Window"

    class buttons:
        pass

    def __init__(self, window: "Window"):
        self.window = window

    @property
    def name(self):
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", self.__class__.__name__)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def detect_buttons(self, buttons: List[Button] = None):
        screenshot = self.window.screenshot(save_path="assets")

        if buttons is None:
            for name, button in vars(self.buttons).items():
                if isinstance(button, Button):
                    button.detect(screenshot)
        else:
            for button in buttons:
                button.detect(screenshot)

    def show_buttons(self, screenshot):
        for name, button in vars(self.buttons).items():
            if isinstance(button, Button):
                x, y, w, h = button.rect
                cv2.rectangle(screenshot, (x, y), (x + w, y + h), (255, 0, 255), 2)

        show_image(screenshot)

    def zoom_out(self):
        center = self.window.center

        # scroll
        pag.moveTo(center["x"], center["y"])
        for _ in range(100):
            pag.scroll(-100)
