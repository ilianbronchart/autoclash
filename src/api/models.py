from typing import Tuple
import pyautogui as pag
import pygetwindow as gw

class Button:
    def __init__(self, window: gw.Window, rect: Tuple[int, int, int, int]):
        self.window = window
        self.rect = rect

    def click(self):
        center_x = self.window.left + self.rect[0] + self.rect[2] // 2
        center_y = self.window.top + self.rect[1] + self.rect[3] // 2
        pag.moveTo(center_x, center_y)
        print(center_x, center_y)
        pag.click()