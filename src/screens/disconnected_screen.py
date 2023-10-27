from typing import List
from src.models.screen import Screen
from src.models.button import Button


class DisconnectedScreen(Screen):
    words: List[str] = [
        "anyone",
        "there",
        "you",
        "have",
        "been",
        "disconnected",
        "due",
        "to",
        "inactivity",
    ]

    class buttons:
        pass
