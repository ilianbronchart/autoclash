import cv2
import re
import pyautogui as pag
from typing import List
from src.models.button import Button
from src.utils import show_image
from typing import TYPE_CHECKING
from time import sleep


if TYPE_CHECKING:
    from src.models.window import Window


class Screen:
    words: List[str]
    window: 'Window'

    class buttons:
        pass


    def __init__(self, window: 'Window'):
        self.window = window


    @property
    def name(self):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__class__.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


    def detect_buttons(self, buttons: List[Button] = None):
        screenshot = self.window.screenshot(save_path='assets')

        if buttons is None:
            for name, button in vars(self.buttons).items():
                if isinstance(button, Button):
                    button.detect(screenshot)
        else:
            for button in buttons:
                button.detect(screenshot)

    
    def show_buttons(self, screenshot):
        for name, button  in vars(self.buttons).items():
            if isinstance(button, Button):
                x, y, w, h = button.rect
                cv2.rectangle(screenshot, (x, y), (x + w, y + h), (255, 0, 255), 2)

        show_image(screenshot)

    
    def zoom_out(self):
        center = self.window.center

        # scroll
        pag.moveTo(center['x'], center['y'])
        for _ in range(100):
            pag.scroll(-100)

    
class MainScreen(Screen):
    words: List[str] = ['attack', 'shop']

    class buttons():
        ATTACK_BUTTON = Button("attack_button")
        TRAIN_BUTTON = Button("train_button")
        ELIXIR_POPUP = Button("elixir_popup")
        GOLD_POPUP = Button("gold_popup")


    def __init__(self, window: 'Window'):
        super().__init__(window)
    
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

    def start_attack(self) -> 'MultiplayerScreen':
        self.buttons.ATTACK_BUTTON.click(self.window)
        pag.sleep(1)
        next_screen = self.window.detect_screen()
        return next_screen


class AttackScreen(Screen):
    words: List[str] = ['tap', 'or', 'press', 'and', 'hold', 'to', 'deploy', 'troops', 'end', 'battle', 'available', 'loot']

    class buttons:
        NEXT_ATTACK_BUTTON = Button("next_attack_button")
        END_BATTLE_BUTTON = Button("end_battle_button")

    def __init__(self, window: 'Window'):
        super().__init__(window)

    def next_attack(self, times: int = 1):
        print(f"window: {self}, times: {times}")
        for _ in range(times):
            self.buttons.NEXT_ATTACK_BUTTON.click(self.window)
            sleep(5)

            
    def end_battle(self):
        self.buttons.END_BATTLE_BUTTON.click(self.window)


class TrainingScreen(Screen):
    words: List[str] = ['train', 'troops', 'army', 'brew', 'spells', 'quick', 'train']

    class buttons:
        QUICK_TRAIN_BUTTON = Button("quick_train_button")
        CLOSE_BUTTON = Button("close_button")


    def __init__(self, window: 'Window'):
        super().__init__(window)


class QuickTrainingScreen(Screen):
    words: List[str] = ['quick', 'train', 'previous', 'army', 'edit']

    class buttons:
        pass

    def __init__(self, window: 'Window'):
        super().__init__(window)


class DisconnectedScreen(Screen):
    words: List[str] = ['anyone', 'there', 'you', 'have', 'been', 'disconnected', 'due', 'to', 'inactivity']

    class buttons:
        pass

    def __init__(self, window: 'Window'):
        super().__init__(window)



class MultiplayerScreen(Screen):
    words: List[str] = ['unranked', 'practice', 'single', 'player']

    class Buttons:
        CLOSE_BUTTON = Button("close_button")
        FIND_MATCH_BUTTON = Button("find_match_button")

    def __init__(self, window: 'Window'):
        super().__init__(window)

