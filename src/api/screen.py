import cv2
import re
from enum import Enum
from typing import List
from src.api.button import Button
from src.utils import show_image
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.api.window import Window


class Screen:
    words: List[str]
    window: 'Window'

    class buttons(Enum):
        pass


    def __init__(self, window: 'Window'):
        self.window = window


    @property
    def name(self):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', self.__class__.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


    def detect_buttons(self, screenshot):
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        for button in self.Buttons:
            button.value.detect(screenshot_gray)


    def show_buttons(self, screenshot):
        for button in self.buttons.values():
            x, y, w, h = button.rect
            cv2.rectangle(screenshot, (x, y), (x + w, y + h), (255, 0, 255), 2)

        show_image(screenshot)

    
class MainScreen(Screen):
    words: List[str] = ['attack', 'shop']

    class buttons(Enum):
        ATTACK_BUTTON = Button("attack_button")
        TRAIN_BUTTON = Button("train_button")
        ELIXIR_POPUP = Button("elixir_popup")
        GOLD_POPUP = Button("gold_popup")

    
    def __init__(self, window: 'Window'):
        super().__init__(window)

    
    def collect_resources(self):
        pass

    
    def has_resources(self):
        screenshot = self.window.screenshot()

        self.detect_buttons


class AttackScreen(Screen):
    words: List[str] = ['tap', 'or', 'press', 'and', 'hold', 'to', 'deploy', 'troops', 'end', 'battle', 'available', 'loot']

    class buttons(Enum):
        NEXT_ATTACK_BUTTON = Button("next_attack_button")
        END_BATTLE_BUTTON = Button("end_battle_button")

    def __init__(self, window: 'Window'):
        super().__init__(window)



class TrainingScreen(Screen):
    words: List[str] = ['train', 'troops', 'army', 'brew', 'spells', 'quick', 'train']

    class buttons(Enum):
        QUICK_TRAIN_BUTTON = Button("quick_train_button")
        CLOSE_BUTTON = Button("close_button")


    def __init__(self, window: 'Window'):
        super().__init__(window)


class DisconnectedScreen(Screen):
    words: List[str] = ['anyone', 'there', 'you', 'have', 'been', 'disconnected', 'due', 'to', 'inactivity']

    class buttons(Enum):
        pass

    def __init__(self, window: 'Window'):
        super().__init__(window)



class MultiplayerScreen(Screen):
    words: List[str] = ['unranked', 'practice', 'single', 'player']

    class Buttons(Enum):
        CLOSE_BUTTON = Button("close_button")
        FIND_MATCH_BUTTON = Button("find_match_button")

    def __init__(self, window: 'Window'):
        super().__init__(window)

