from src.models.base import Rect
from src.models.window import Window
from src.models.screen import MainScreen, AttackScreen, TrainingScreen
from src.config import Model
import src.tesseract as tess
from src.textdetection import detect_text
from dotenv import load_dotenv
from src.connected_components import useful_preprocessing_steps
import cv2


def init():
    load_dotenv()
    tess.check_model_exists(Model.BackBeat)
    tess.check_model_exists(Model.SupercellMagic)


def main():
    screenshot = cv2.imread("assets/screenshot.png")

    useful_preprocessing_steps(screenshot)


if __name__ == "__main__":
    main()
