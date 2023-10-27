from typing import List
import cv2
from imutils.object_detection import non_max_suppression
import numpy as np
from src.models.base import Rect
from src.utils import draw_rects

net = cv2.dnn.readNet("assets/models/frozen_east_text_detection.pb")


class TextDetectionResult:
    COALESCE_THRESHOLD: int = 20
    rects: List[Rect]
    img: np.ndarray

    def __init__(self, rects, img):
        self.rects = rects
        self.img = img

        self.coalesce()
        

    def draw(self):
        draw_rects(self.img, self.rects)


    def coalesce(self):
        i = 0
        
        while i < len(self.rects):
            rect1 = self.rects[i]
            merged = False

            for j in range(len(self.rects)):
                if i != j:
                    rect2 = self.rects[j]
                    
                    if rect1.close_to(rect2, self.COALESCE_THRESHOLD):
                        new_rect = rect1.merge(rect2)
                        self.rects[i] = new_rect
                        del self.rects[j]
                        merged = True
                        break

            if not merged:
                i += 1


def preprocess_image(img):
    orig = img.copy()
    H, W = img.shape[:2]

    newH = int(round(H / 32) * 32)
    newW = newH * 2
    rW = W / float(newW)
    rH = H / float(newH)
    
    img = cv2.resize(img, (newW, newH))
    blob = cv2.dnn.blobFromImage(img, 1.0, (newW, newH),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    
    return blob, rW, rH


def detect_text_regions(blob, net, layerNames=["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]):
    net.setInput(blob)
    scores, geometry = net.forward(layerNames)
    return scores, geometry


def post_process(scores, geometry, rW, rH, padding_x=0.05, padding_y=0.25) -> List[Rect]:
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    for y in range(0, numRows):
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        for x in range(0, numCols):
            if scoresData[x] < 0.5:
                continue

            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            width_padding = int(w * padding_x)
            height_padding = int(h * padding_y)

            rects.append((startX - width_padding, startY - height_padding, 
                          endX + width_padding, endY + height_padding))
            confidences.append(scoresData[x])

    boxes = non_max_suppression(np.array(rects), probs=confidences)
    
    results = []
    for (startX, startY, endX, endY) in boxes:
        x = int(startX * rW)
        y = int(startY * rH)
        w = int((endX - startX) * rW)
        h = int((endY - startY) * rH)
        
        results.append(Rect(x=x, y=y, w=w, h=h))
    
    return results


def detect_text(img) -> TextDetectionResult:
    blob, rW, rH = preprocess_image(img)
    scores, geometry = detect_text_regions(blob, net)
    rects =  post_process(scores, geometry, rW, rH)
    return TextDetectionResult(rects, img)
