from typing import List
from src.models.screen import Screen
from src.models.button import Button


class MultiplayerScreen(Screen):
    words: List[str] = ["unranked", "practice", "single", "player"]

    class Buttons:
        CLOSE_BUTTON = Button("close_button")
        FIND_MATCH_BUTTON = Button("find_match_button")
