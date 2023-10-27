from typing import List
from src.models.screen import Screen
from src.models.button import Button


class TrainingScreen(Screen):
    words: List[str] = ["train", "troops", "army", "brew", "spells", "quick", "train"]

    class buttons:
        QUICK_TRAIN_BUTTON = Button("quick_train_button")
        CLOSE_BUTTON = Button("close_button")
