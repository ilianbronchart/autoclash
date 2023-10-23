import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
import os
from src.config import WINDOW_OFFSET, WINDOW_OFFSET_TOP, REFERENCE_IMAGES_DIR, SIMILARITY_THRESHOLD

def find_and_screenshot_window(window_title, save=False):
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

        if (save):
          cv2.imwrite('assets/window_screenshot.png', screenshot_np)

        pyautogui.sleep(3)
        window.minimize()

        return screenshot_np

    except IndexError:
        print("Window not found. Please ensure the window is open and the title is correct.")
    except Exception as e:
        print("An error occurred:", str(e))

def match_screen(screenshot, reference_image):
    # Convert images to grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    reference_gray = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # Compute ORB keypoints and descriptors
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(screenshot_gray, None)
    kp2, des2 = orb.detectAndCompute(reference_gray, None)

    # Match descriptors
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Compute similarity
    similarity = len(matches) / min(len(kp1), len(kp2))
    return similarity

def recognize_game_screen(screenshot_np):
    for filename in os.listdir(REFERENCE_IMAGES_DIR):
        if filename.endswith('.png'):
            reference_image = cv2.imread(os.path.join(REFERENCE_IMAGES_DIR, filename))
            similarity = match_screen(screenshot_np, reference_image)
            if similarity > SIMILARITY_THRESHOLD:
                return filename.split('.')[0]  # Return the screen name without the file extension

    return "Unknown Screen"