from enum import Enum
import cv2
from typing import List
from src.api.button import Button
from src.utils import show_image

class Screen:
    class buttons(Enum):
        pass

    def __init__(self, name: str, button_names: List[str], words: List[str]):
        self.name = name
        self.words = words

        self.buttons = {}
        for name in button_names:
            self.buttons[name] = Button(name)


    def detect_buttons(self, screenshot):
        for button in self.buttons.values():
            button.detect(screenshot)


    def show_buttons(self, screenshot):
        for button in self.buttons.values():
            x, y, w, h = button.rect
            cv2.rectangle(screenshot, (x, y), (x + w, y + h), (255, 0, 255), 2)

        show_image(screenshot)

    
class MainScreen(Screen):
    class buttons(Enum):
        ATTACK_BUTTON = Button("attack_button")
        TRAIN_BUTTON = Button("train_button")
        ELIXIR_POPUP = Button("elixir_popup")
        GOLD_POPUP = Button("gold_popup")

    def __init__(self, name: str, words: List[str]):
        super().__init__(name, words)

    def collect_resources(self, screenshot):
        pass


class AttackScreen(Screen):
    class Buttons(Enum):
        NEXT_ATTACK_BUTTON = Button("next_attack_button")
        END_BATTLE_BUTTON = Button("end_battle_button")

    def __init__(self, name: str, words: List[str]):
        super().__init__(name, words)
        self.buttons = {button.name: button.value for button in self.Buttons}

class TrainingScreen(Screen):
    class Buttons(Enum):
        QUICK_TRAIN_BUTTON = Button("quick_train_button")
        CLOSE_BUTTON = Button("close_button")

    def __init__(self, name: str, words: List[str]):
        super().__init__(name, words)
        self.buttons = {button.name: button.value for button in self.Buttons}
