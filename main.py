from src.models.base import Rect
from src.models.window import Window
from src.config import Model
import src.vision.tesseract as tess
from dotenv import load_dotenv


def init():
    load_dotenv()
    tess.check_model_exists(Model.BackBeat)
    tess.check_model_exists(Model.SupercellMagic)


def main():
    window = Window()
    window.show()
    screen = window.detect_screen()
    window.hide()


if __name__ == "__main__":
    main()
