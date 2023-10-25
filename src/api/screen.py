import cv2
from typing import List
from src.api.button import Button
from src.utils import show_image

class Screen:
    def __init__(self, name: str, button_names: List[str], words: List[str]):
        self.name = name
        self.words = words

        self.buttons = {}
        for name in button_names:
            self.buttons[name] = Button(name)


    def detect_buttons(self, screenshot):
        for button in self.buttons.values():
            button.detect(screenshot)


    def show_buttons(self, screenshot):
        for button in self.buttons.values():
            x, y, w, h = button.rect
            cv2.rectangle(screenshot, (x, y), (x + w, y + h), (255, 0, 255), 2)

        show_image(screenshot)