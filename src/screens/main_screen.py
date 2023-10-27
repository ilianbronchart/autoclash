from typing import List
from src.models.screen import Screen
from src.models.button import Button
import pyautogui as pag
from src.screens.multiplayer_screen import MultiplayerScreen


class MainScreen(Screen):
    words: List[str] = ["attack", "shop"]

    class buttons:
        ATTACK_BUTTON = Button("attack_button")
        TRAIN_BUTTON = Button("train_button")
        ELIXIR_POPUP = Button("elixir_popup")
        GOLD_POPUP = Button("gold_popup")

    def collect_resources(self):
        self.zoom_out()
        self.detect_buttons([self.buttons.GOLD_POPUP, self.buttons.ELIXIR_POPUP])

        if self.buttons.GOLD_POPUP.is_visible():
            self.buttons.GOLD_POPUP.click(self.window)

        pag.sleep(0.5)

        if self.buttons.ELIXIR_POPUP.is_visible():
            self.buttons.ELIXIR_POPUP.click(self.window)

        pag.sleep(0.5)
        self.detect_buttons()

        # Collect other elixir type (since they have the same-ish button)
        if self.buttons.ELIXIR_POPUP.is_visible():
            self.buttons.ELIXIR_POPUP.click(self.window)

    def start_attack(self) -> "MultiplayerScreen":
        self.buttons.ATTACK_BUTTON.click(self.window)
        pag.sleep(1)
        next_screen = self.window.detect_screen()
        return next_screen
