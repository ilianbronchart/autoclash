from typing import List
from src.models.screen import Screen
from src.models.button import TemplateButton, TextButton


class MultiplayerScreen(Screen):
    words: List[str] = ["unranked", "practice", "single", "player"]

    class Buttons:
        CLOSE_BUTTON = TemplateButton("close_button")
        FIND_MATCH_BUTTON = TextButton("match")
