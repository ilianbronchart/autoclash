from src.api.models.window import Window
from src.api.models.screen import MainScreen, AttackScreen, TrainingScreen
from src.utils import draw_boxes
from src.config import Model
from src.tesseract import check_model_exists, image_to_data
from dotenv import load_dotenv

def init():
    load_dotenv()
    check_model_exists(Model.BackBeat)


def main():
    init()

    window = Window()
    window.show()

    screenshot = window.screenshot()
    image_to_data(screenshot, Model.BackBeat)



if __name__ == '__main__':
    main()