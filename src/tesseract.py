import pytesseract as tess
import cv2
import os
from src.config import OCR_WHITE_THRESHOLD, Model
from src.utils import filter_small_components, draw_boxes
from pathlib import Path
import shutil


def image_to_string(image, model: Model):
    return tess.image_to_string(image, config=f"--psm 4 --oem 3 -l {model.value}")


def image_to_data(image, model: Model):
    image = preprocess_image(image)
    data = tess.image_to_data(image, config=f"--psm 4 --oem 3 -l {model.name}", output_type=tess.Output.DICT)
    
    boxes = []
    for i in range(len(data['level'])):
        if data['level'][i] == 5:  # Word level
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            boxes.append((x, y, w, h))

    draw_boxes(image, boxes)

    return boxes


def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)

    return invert


def detect_text_no_pre(screenshot, model: Model):
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    return image_to_string(gray, model)


def detect_text_thresholded(screenshot, model: Model):
    # Convert image to grayscale
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    # Keep pixels above the threshold (retain different shades of gray)
    thresholded = cv2.inRange(gray, OCR_WHITE_THRESHOLD, 255)

    # Filter out small components
    filtered = filter_small_components(thresholded)

    return image_to_string(filtered, model)


def check_model_exists(model: str):
    tessdata_path = os.environ.get("TESSDATA_PATH")
    
    if tessdata_path is None:
        raise EnvironmentError("TESSDATA_PATH environment variable is not set")
    
    if not os.path.isdir(tessdata_path):
        raise FileNotFoundError(f"The directory specified in TESSDATA_PATH does not exist: {tessdata_path}")
    
    model_path = os.path.join(tessdata_path, f"{model.value}.traineddata")
    if not os.path.isfile(model_path):
        print(f"The model {model.value}.traineddata does not exist in the directory {tessdata_path}")
        
        src_model_path = Path("tesseract/models", f"{model.value}.traineddata")
        if src_model_path.is_file():
            shutil.copy(src_model_path, tessdata_path)
            print(f"{model.value} has been successfully installed!")
        else:
            raise FileNotFoundError(f"The model {model.value}.traineddata does not exist in the tesseract/models directory.")