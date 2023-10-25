from src.api.window import Window
from src.api.screen import Screen


disconnected_screen = Screen(
    name='disconnected_screen', 
    words=['anyone', 'there', 'you', 'have', 'been', 'disconnected', 'due', 'to', 'inactivity']
)
multiplayer_screen = Screen(
    name='multiplayer_screen', 
    words=['unranked', 'practice', 'single', 'player']
)
main_screen = MainScreen(
    name='main_screen', 
    words=['attack', 'shop']
)
attack_screen = AttackScreen(
    name='attack_screen', 
    words=['tap', 'or', 'press', 'and', 'hold', 'to', 'deploy', 'troops', 'end', 'battle', 'available', 'loot']
)
training_screen = TrainingScreen(
    name='training_screen', 
    words=['train', 'troops', 'army', 'brew', 'spells', 'quick', 'train']
)

window = Window([
    disconnected_screen,
    multiplayer_screen,
    main_screen,
    attack_screen,
    training_screen
])

 

screen.buttons['attack_button'].click()

screen.buttons.attack.click()