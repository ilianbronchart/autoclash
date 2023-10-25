import pyautogui as pag
import pygetwindow as gw
import cv2
import numpy as np
import re
from typing import List
from src.api.screen import Screen, MainScreen, AttackScreen, TrainingScreen, DisconnectedScreen, MultiplayerScreen
from src.utils import detect_text_thresholded, detect_text_no_pre
from src.config import OCR_SAMPLES


class Window:
    screens: List[Screen]
    WINDOW_TITLE: str = 'Clash of Clans'
    SCREENSHOT_OUTER_BORDER: int = 10
    SCREENSHOT_HEADER_SIZE: int = 32


    def __init__(self):
        windows = gw.getWindowsWithTitle(self.WINDOW_TITLE)
        if not windows:
            raise ValueError("Window not found. Please ensure the window is open and the title is correct.")
        self.window = windows[0]

        self.screens = [
            MainScreen(self),
            AttackScreen(self),
            TrainingScreen(self),
            DisconnectedScreen(self),
            MultiplayerScreen(self)
        ]
    
    
    def show(self):
        try:
            self.window.activate()
        except:
            pass
        self.window.restore()

    
    def hide(self):
        self.window.minimize()


    def screenshot(self, num_screenshots=1, save_path=None):
        rect = self.window._rect  # using _rect to get all bounds in one call
        region = (
            rect.x + self.SCREENSHOT_OUTER_BORDER, 
            rect.y + self.SCREENSHOT_HEADER_SIZE,
            rect.w - 2 * self.SCREENSHOT_OUTER_BORDER, 
            rect.h - self.SCREENSHOT_OUTER_BORDER - self.SCREENSHOT_HEADER_SIZE
        )
        screenshots = []
        
        for i in range(num_screenshots):
            pag.sleep(0.3)
            screenshot = pag.screenshot(region=region)
            screenshot = np.array(screenshot)

            # Changed the color conversion flag to convert from RGB to BGR
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
            screenshots.append(screenshot)

            if save_path:
                cv2.imwrite(f"{save_path}/screenshot_{i + 1}.png", screenshot)

        return screenshots
    

    def detect_screen(self):
        screenshots = self.screenshot(OCR_SAMPLES)
        words = self.compile_text_samples(screenshots) 
        return self.detect_screen_from_words(words)
    

    def compile_text_samples(self, screenshots):
        detected_texts = set()

        texts = []

        for screenshot in screenshots:
            texts.append(detect_text_thresholded(screenshot))

        for _, i in enumerate(range(2)):
            texts.append(detect_text_no_pre(screenshots[i]))

        for text in texts:
            text = text.replace('\n', ' ')
            text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text).lower()  # Keep only alphanumeric characters and spaces, then convert to lowercase
            
            for word in text.split():
                detected_texts.add(word)
        
        return detected_texts


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