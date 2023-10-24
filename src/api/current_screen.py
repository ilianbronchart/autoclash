import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
from src.utils import show_image
from src.config import OCR_WHITE_THRESHOLD, SCREEN_TEXT, WINDOW_TITLE
import pyautogui
import pytesseract
import re


def get_window():
    windows = gw.getWindowsWithTitle(WINDOW_TITLE)
    if not windows:
        raise ValueError("Window not found. Please ensure the window is open and the title is correct.")
    return windows[0]

def screenshot_window(window, num_screenshots=1):
    window.activate()
    window.restore()

    rect = window._rect  # using _rect to get all bounds in one call
    region = (rect.x, rect.y, rect.w, rect.h)
    
    screenshots = []
    for _ in range(num_screenshots):
        pyautogui.sleep(0.3)
        screenshot = pyautogui.screenshot(region=region)
        screenshot_np = np.array(screenshot)
        # Changed the color conversion flag to convert from RGB to BGR
        screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        screenshots.append(screenshot_np)

    window.minimize()

    return screenshots


def compile_text_samples(screenshots):
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


def detect_text_no_pre(screenshot_np):
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    return pytesseract.image_to_string(screenshot_np)

def filter_small_components(binary_img, min_area=50):
    """
    Remove small connected components from a binary image based on a given area threshold.
    """
    # Find all connected components
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_img, connectivity=8)
    
    # Create an output image, initialized as all zeros (black)
    output = np.zeros_like(binary_img)
    
    # Loop through all connected component labels
    for i in range(1, num_labels):
        # If the area of the connected component is above the threshold, add it to the output image
        if stats[i, cv2.CC_STAT_AREA] > min_area:
            output[labels == i] = 255
            
    return output

def detect_text_thresholded(screenshot_np, show_cleaned=False):
    # Convert image to grayscale
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    
    # Keep pixels above the threshold (retain different shades of gray)
    thresholded = cv2.inRange(gray, OCR_WHITE_THRESHOLD, 255)

    # Filter out small components
    filtered = filter_small_components(thresholded)
    
    if show_cleaned:
        show_image(filtered)
    
    return pytesseract.image_to_string(filtered)

def detect_screen(words):
    # Filter out words that are not in any include list
    valid_words = set(word for screen_data in SCREEN_TEXT.values() for word in screen_data)
    filtered_words = set(words) & valid_words
    
    max_matches = 0
    likely_screen = None
    
    for screen, criteria in SCREEN_TEXT.items():
        matching_words = set(criteria) & filtered_words
        match_ratio = len(matching_words) / len(criteria)
        
        # Update likely screen if a higher match ratio is found
        if match_ratio > max_matches:
            max_matches = match_ratio
            likely_screen = screen
            
        # Optional: If a screen's criteria fully matches, you could break out early for efficiency
        if match_ratio == 1:
            break

    # Return the screen with the highest match ratio
    return likely_screen