import pyautogui as pag
import pygetwindow as gw
import cv2
import numpy as np
from typing import Tuple
import os
from src.config import TEMPLATES_DIR
from src.utils import rescale_template


INVISIBLE = (0, 0, 0, 0)


class Button:
    def __init__(self, name: str, rect: Tuple[int, int, int, int] = INVISIBLE):
        self.name = name
        self.rect = rect
        self.template = cv2.imread(os.path.join(TEMPLATES_DIR, f"{self.name}.png"))


    def click(self, window):
        assert self.is_visible(), f"Button {self.name} is not visible"

        center_x = window.position['x'] + self.rect[0] + self.rect[2] // 2
        center_y = window.position['y'] + self.rect[1] + self.rect[3] // 2
        pag.moveTo(center_x, center_y)
        pag.click()


    def detect(self, screenshot):
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)

        # Rescale the template based on the screenshot size
        target_screenshot_size = (screenshot.shape[1], screenshot.shape[0])  # Shape returns (height, width), so we reverse it
        rescaled_template = rescale_template(template_gray, target_screenshot_size)
        
        # Get dimensions of the rescaled template
        h, w = rescaled_template.shape
        
        # Perform template matching
        result = cv2.matchTemplate(screenshot_gray, rescaled_template, cv2.TM_CCOEFF_NORMED)
        
        # Set a threshold value to consider a match
        threshold = 0.7
        loc = np.where(result >= threshold)
        
        # If no match is found, return None
        if len(loc[0]) == 0:
            return INVISIBLE

        # Get the location of the first match
        for pt in zip(*loc[::-1]):
            self.rect = (pt[0], pt[1], w, h)
            return
        
    
    def detect_with_sift(self, screenshot):
        # Convert images to grayscale
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)

        # Initialize SIFT detector
        sift = cv2.SIFT_create()

        # Find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(screenshot_gray, None)
        kp2, des2 = sift.detectAndCompute(template_gray, None)

        # Use FLANN based matcher
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        # Store all the good matches using Lowe's ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > 10:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            # Define bounding box around matched keypoints
            x_coords = [p[0][0] for p in src_pts]
            y_coords = [p[0][1] for p in src_pts]
            x, y, w, h = min(x_coords), min(y_coords), max(x_coords) - min(x_coords), max(y_coords) - min(y_coords)
            
            return (x, y, w, h)
        else:
            return INVISIBLE
        
    
    def detect_with_sift(self, screenshot):
        # Convert images to grayscale
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)

        # Initialize SURF detector
        surf = cv2.xfeatures2d.SURF_create()

        # Find the keypoints and descriptors with SURF
        kp1, des1 = surf.detectAndCompute(screenshot_gray, None)
        kp2, des2 = surf.detectAndCompute(template_gray, None)

        # Use FLANN based matcher
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        # Store all the good matches using Lowe's ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > 10:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            # Define bounding box around matched keypoints
            x_coords = [p[0][0] for p in src_pts]
            y_coords = [p[0][1] for p in src_pts]
            x, y, w, h = min(x_coords), min(y_coords), max(x_coords) - min(x_coords), max(y_coords) - min(y_coords)
            
            return (x, y, w, h)
        else:
            return INVISIBLE
        

    # def detect(self, screenshot):
    #     screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    #     template_gray = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)

    #     # Initialize ORB detector
    #     orb = cv2.ORB_create()

    #     # Find the keypoints and descriptors with ORB
    #     kp1, des1 = orb.detectAndCompute(screenshot_gray, None)
    #     kp2, des2 = orb.detectAndCompute(template_gray, None)

    #     # Check if descriptors are None or empty
    #     if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
    #         return INVISIBLE

    #     # Ensure both descriptors are of the same type, here we convert them to float32
    #     if des1.dtype != np.float32:
    #         des1 = np.float32(des1)
    #     if des2.dtype != np.float32:
    #         des2 = np.float32(des2)

    #     # Use brute force matcher
    #     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    #     matches = bf.match(des1, des2)
    #     matches = sorted(matches, key=lambda x: x.distance)

    #     # If we have enough good matches, we assume we found the object
    #     print(len(matches))
    #     if len(matches) > 10:
    #         src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)

    #         # Define bounding box around matched keypoints
    #         x_coords = [p[0][0] for p in src_pts]
    #         y_coords = [p[0][1] for p in src_pts]
    #         x, y, w, h = min(x_coords), min(y_coords), max(x_coords) - min(x_coords), max(y_coords) - min(y_coords)

    #         print((x,y,w,h))
    #         return (x, y, w, h)
    #     else:
    #         return INVISIBLE



        
    def is_visible(self):
        return self.rect != INVISIBLE