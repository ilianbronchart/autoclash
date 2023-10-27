from typing import List
import pytesseract as tess
import cv2
import os
from src.config import Model
from src.models.base import Rect, TextRect
from src.utils import show_image
from pathlib import Path
import shutil
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import re


class OCRResult:
    current_window = None
    text_rects: List[TextRect]
    img: np.ndarray

    def __init__(self, text_rects, img):
        self.text_rects = text_rects
        self.img = img
        # self.filter()
        self.clean_text()

    @property
    def rects(self):
        return [text_rect.rect for text_rect in self.text_rects]

    @property
    def text(self):
        return "\n".join([text_rect.text for text_rect in self.text_rects])

    def filter(self):
        text_rects = []

        for text_rect in self.text_rects:
            if len(text_rect.text) > 0:
                text_rects.append(text_rect)

        self.text_rects = text_rects

    def clean_text(self):
        for text_rect in self.text_rects:
            text_rect.text = text_rect.text.replace("\n", "")
            text_rect.text = text_rect.text.lower()
            text_rect.text = re.sub(r"[^a-z0-9\s/]", "", text_rect.text)

    def on_mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            for text_rect in param["text_rects"]:
                rect = text_rect.rect

                if rect.x <= x <= rect.x + rect.w and rect.y <= y <= rect.y + rect.h:
                    if self.current_window:
                        try:
                            cv2.destroyWindow(self.current_window)
                        except:
                            pass

                    self.current_window = "Text Image"
                    cv2.imshow(self.current_window, text_rect.img)
                    cv2.waitKey(
                        1
                    )  # Add a small delay to allow the window to be created

    def draw(
        self,
        img=None,
        font_scale: float = 0.5,
        font_thickness: int = 1,
        text_color: tuple = (0, 255, 255),
        padding: int = 5,
    ):
        if img is None:
            img = self.img.copy()

        # Set font type
        font = cv2.FONT_HERSHEY_SIMPLEX

        for text_rect in self.text_rects:
            # Draw filled rectangle with black color
            pt1 = (text_rect.rect.x, text_rect.rect.y)
            pt2 = (
                text_rect.rect.x + text_rect.rect.w,
                text_rect.rect.y + text_rect.rect.h,
            )
            cv2.rectangle(img, pt1, pt2, (0, 0, 0), -1)

            # Get the text size
            (text_width, text_height) = cv2.getTextSize(
                text_rect.text, font, font_scale, font_thickness
            )

            # Calculate text position
            x = text_rect.rect.x + padding
            y = text_rect.rect.y + padding + text_height + 10

            # Draw text
            cv2.putText(
                img,
                text_rect.text,
                (x, y),
                font,
                font_scale,
                text_color,
                font_thickness,
                cv2.LINE_AA,
            )

        cv2.imshow("Image", img)
        cv2.setMouseCallback(
            "Image", self.on_mouse_click, {"text_rects": self.text_rects}
        )
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __str__(self):
        return "\n".join([text_rect.text for text_rect in self.text_rects])


def process_rect(rect: Rect, img, model) -> TextRect:
    x, y, w, h = rect
    text_img = img[y : y + h, x : x + w]

    text_img = cv2.resize(text_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    text = tess.image_to_string(text_img, config=f"-l {model.value} --psm 8")
    return TextRect(text=text, rect=rect, img=text_img)


def rect_to_digits(img, rect) -> TextRect:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)
    thresh = cv2.threshold(invert, 25, 255, cv2.THRESH_BINARY)[1]

    x, y, w, h = rect
    text_img = thresh[y : y + h, x : x + w]

    text_img = cv2.resize(text_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    text = tess.image_to_string(
        text_img,
        lang="SupercellMagic",
        config="--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789",
    )

    return OCRResult([TextRect(text=text, rect=rect, img=text_img)], img)


def extract_digits(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)

    # Apply thresholding to get a binary image
    thresh = cv2.threshold(invert, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Show the contour mask
    cv2.imshow("Contour Mask", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def rects_to_text(img, rects: List[Rect], model: Model) -> OCRResult:
    text_rects = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Using ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor() as executor:
        # Creating a dictionary to hold the futures
        futures = {
            executor.submit(process_rect, rect, gray, model): rect for rect in rects
        }

        # Using tqdm to show a progress bar
        for future in tqdm(
            as_completed(futures),
            total=len(rects),
            desc="Processing Rectangles",
            unit="rect",
        ):
            rect = futures[future]
            try:
                # Getting the result of the future
                text_rect = future.result()
                text_rects.append(text_rect)
            except Exception as exc:
                print(f"Rectangle {rect} generated an exception: {exc}")

    return OCRResult(text_rects, img)


def check_model_exists(model: str):
    tessdata_path = os.environ.get("TESSDATA_PATH")

    if tessdata_path is None:
        raise EnvironmentError("TESSDATA_PATH environment variable is not set")

    if not os.path.isdir(tessdata_path):
        raise FileNotFoundError(
            f"The directory specified in TESSDATA_PATH does not exist: {tessdata_path}"
        )

    model_path = os.path.join(tessdata_path, f"{model.value}.traineddata")
    if not os.path.isfile(model_path):
        print(
            f"The model {model.value}.traineddata does not exist in the directory {tessdata_path}"
        )

        src_model_path = Path("tesseract/models", f"{model.value}.traineddata")
        if src_model_path.is_file():
            shutil.copy(src_model_path, tessdata_path)
            print(f"{model.value} has been successfully installed!")
        else:
            raise FileNotFoundError(
                f"The model {model.value}.traineddata does not exist in the tesseract/models directory."
            )
