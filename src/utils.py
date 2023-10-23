import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
from time import sleep
from config import OFFSET, OFFSET_TOP

def find_and_screenshot_window(window_title):
    try:
        # Find the window by its title
        window = gw.getWindowsWithTitle(window_title)[0]
                
        # Wait a moment for the window to minimize
        pyautogui.sleep(1)

        # Restore the window (bring to front)
        window.restore()
        
        # Wait a moment for the window to restore
        pyautogui.sleep(1)

        # Define the region to capture (excluding the top bar)
        region = (window.left + OFFSET, window.top + OFFSET_TOP, window.width - 2 * OFFSET, window.height - OFFSET_TOP - OFFSET)

        # Take a screenshot of the window's contents
        screenshot = pyautogui.screenshot(region=region)
        
        # Convert the screenshot to a NumPy array
        screenshot_np = np.array(screenshot)
        
        # Convert the color space from BGR to RGB
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
        
        # Save the screenshot
        cv2.imwrite('window_screenshot.png', screenshot_np)

        sleep(2)
        window.minimize()

        
        print("Screenshot taken and saved as 'window_screenshot.png'")
        
    except IndexError:
        print("Window not found. Please ensure the window is open and the title is correct.")
    except Exception as e:
        print("An error occurred:", str(e))