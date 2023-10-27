from src.models.window import Window
from src.models.screen import MainScreen, AttackScreen, TrainingScreen
from src.config import Model
import src.tesseract as tess
from src.textdetection import detect_text
from dotenv import load_dotenv

def init():
    load_dotenv()
    tess.check_model_exists(Model.BackBeat)
    tess.check_model_exists(Model.SupercellMagic)


def main():
    init()

    window = Window()
    window.show()

    screenshot = window.screenshot()
    window.hide()

    result = detect_text(screenshot)

    result = tess.rects_to_text(screenshot, result.rects, Model.Eng)
    print(result.text)
    result.draw()




if __name__ == '__main__':
    main()