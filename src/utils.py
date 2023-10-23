import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
from src.config import WINDOW_OFFSET, WINDOW_OFFSET_TOP

def find_and_screenshot_window(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]      
        pyautogui.sleep(1)
        window.restore()
        pyautogui.sleep(1)

        region = (
          window.left + WINDOW_OFFSET,
          window.top + WINDOW_OFFSET_TOP, 
          window.width - 2 * WINDOW_OFFSET, 
          window.height - WINDOW_OFFSET_TOP - WINDOW_OFFSET
        )

        screenshot = pyautogui.screenshot(region=region)
        screenshot_np = np.array(screenshot)
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
        cv2.imwrite('assets/window_screenshot.png', screenshot_np)

        pyautogui.sleep(3)
        window.minimize()

    except IndexError:
        print("Window not found. Please ensure the window is open and the title is correct.")
    except Exception as e:
        print("An error occurred:", str(e))