from typing import List
from src.models.screen import Screen
from src.models.button import Button
from time import sleep


class AttackScreen(Screen):
    words: List[str] = [
        "tap",
        "or",
        "press",
        "and",
        "hold",
        "to",
        "deploy",
        "troops",
        "end",
        "battle",
        "available",
        "loot",
    ]

    class buttons:
        NEXT_ATTACK_BUTTON = Button("next_attack_button")
        END_BATTLE_BUTTON = Button("end_battle_button")

    def next_attack(self, times: int = 1):
        print(f"window: {self}, times: {times}")
        for _ in range(times):
            self.buttons.NEXT_ATTACK_BUTTON.click(self.window)
            sleep(5)

    def end_battle(self):
        self.buttons.END_BATTLE_BUTTON.click(self.window)
