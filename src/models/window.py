import pyautogui as pag
import pygetwindow as gw
import cv2
import numpy as np
from typing import List
from src.screens import *
from src.models.screen import Screen
from src.models.base import Rect
from src.vision.textdetection import detect_text, TextDetectionResult
import src.vision.preprocessing as preprocessing
import src.vision.tesseract as tess
from src.config import Model


class Window:
    screens: List[Screen]
    WINDOW_TITLE: str = "Clash of Clans"
    SCREENSHOT_OUTER_BORDER: int = 10
    SCREENSHOT_HEADER_SIZE: int = 32

    def __init__(self):
        windows = gw.getWindowsWithTitle(self.WINDOW_TITLE)
        if not windows:
            raise ValueError(
                "Window not found. Please ensure the window is open and the title is correct."
            )
        self.window = windows[0]

        self.screens = [
            MainScreen(self),
            AttackScreen(self),
            TrainingScreen(self),
            DisconnectedScreen(self),
            MultiplayerScreen(self),
            QuickTrainingScreen(self),
        ]

    @property
    def rect(self) -> Rect:
        return Rect(
            x=self.window.left + self.SCREENSHOT_OUTER_BORDER,
            y=self.window.top + self.SCREENSHOT_HEADER_SIZE,
            w=self.window.width - 2 * self.SCREENSHOT_OUTER_BORDER,
            h=self.window.height
            - self.SCREENSHOT_OUTER_BORDER
            - self.SCREENSHOT_HEADER_SIZE,
        )

    def show(self):
        try:
            self.window.activate()
        except:
            pass
        self.window.restore()
        pag.sleep(1)

    def hide(self):
        self.window.minimize()

    def screenshot(self, save_path=None):
        x, y, w, h = self.rect
        screenshot = pag.screenshot(region=(x, y, w, h))
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        if save_path:
            cv2.imwrite(save_path, screenshot)

        return screenshot

    def detect_screen(self):
        screenshot = self.screenshot()

        # TODO optimize this, text detection might need a less intensive preprocesing step
        img = preprocessing.extract_white_text(screenshot)
        text_detection: TextDetectionResult = detect_text(img)
        ocr = tess.rects_to_text(img, text_detection.rects, Model.BackBeat)

        # return self.detect_screen_from_words(words)

    def detect_screen_from_words(self, words: List[str]) -> Screen:
        # Filter out words that are not in any include list
        valid_words = set(word for screen in self.screens for word in screen.words)
        filtered_words = set(words) & valid_words

        max_matches = 0
        likely_screen = None

        for screen in self.screens:
            matching_words = set(screen.words) & filtered_words
            match_ratio = len(matching_words) / len(screen.words)

            # Update likely screen if a higher match ratio is found
            if match_ratio > max_matches:
                max_matches = match_ratio
                likely_screen = screen

            # Optional: If a screen's criteria fully matches, you could break out early for efficiency
            if match_ratio == 1:
                break

        return likely_screen
