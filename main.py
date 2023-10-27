from src.models.base import Rect
from src.models.window import Window
from src.models.screen import MainScreen, AttackScreen, TrainingScreen
from src.config import Model
import src.tesseract as tess
from src.textdetection import detect_text
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
    img = window.screenshot()
    window.hide()

    img = preprocessing.extract_white_text(img)

    result = detect_text(img)
    result.draw()

    result = tess.rects_to_text(img, result.rects, Model.Eng)
    # result.draw()


if __name__ == "__main__":
    main()
