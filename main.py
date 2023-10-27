from src.models.base import Rect
from src.models.window import Window
from src.config import Model
import src.vision.tesseract as tess
from src.vision.textdetection import detect_text
import src.vision.preprocessing as preprocessing
from src.utils import show_image
from dotenv import load_dotenv
import cv2


def init():
    load_dotenv()
    tess.check_model_exists(Model.BackBeat)
    tess.check_model_exists(Model.SupercellMagic)


def main():
    window = Window()
    window.show()
    screenshot = window.screenshot("assets/screens/")
    window.hide()

    # processed = preprocessing.extract_white_text(screenshot)
    # result = detect_text(processed)

    # result = tess.rects_to_text(processed, result.rects, Model.BackBeat)
    # result.draw(screenshot)


if __name__ == "__main__":
    main()
