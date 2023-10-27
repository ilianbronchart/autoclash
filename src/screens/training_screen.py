from typing import List
from src.models.screen import Screen
from src.models.button import TemplateButton, TextButton


class TrainingScreen(Screen):
    words: List[str] = ["train", "troops", "army", "brew", "spells", "quick", "train"]

    class buttons:
        QUICK_TRAIN_BUTTON = TextButton("quick train")
        CLOSE_BUTTON = TemplateButton("close_button")
