import cv2
import os
import pytest

from src.api.models.buttons import detect_button

# Directory containing the test screenshots
SCREENSHOTS_DIR = "./test/screenshots" 

@pytest.mark.parametrize(os.listdir(SCREENSHOTS_DIR))
def test_detect_screen(screenshot_name):
    # Load the screenshot
    screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
    screenshot = cv2.imread(screenshot_path)

    # Use the detect_button function
    detected_screen = detect_button(screenshot)

    # Remove file extension from the screenshot_name to get expected screen name
    expected_screen = os.path.splitext(screenshot_name)[0]

    # Assert that detected screen matches the expected screen
    assert detected_screen == expected_screen, f"Expected {expected_screen}, but got {detected_screen}"
