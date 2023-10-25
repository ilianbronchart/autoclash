from src.api.window import Window
from src.api.screen import Screen


window = Window([
    Screen(
        name='disconnected_screen', 
        button_names=[], 
        words=['anyone', 'there', 'you', 'have', 'been', 'disconnected', 'due', 'to', 'inactivity']
    ),
    Screen(
        name='multiplayer_screen', 
        button_names=['close_button', 'find_match_button'], 
        words=['unranked', 'practice', 'single', 'player']
    ),
    Screen(
        name='main_screen', 
        button_names=['attack_button', 'main_train_button', 'elixir_popup', 'gold_popup'], 
        words=['attack', 'shop']
    ),
    Screen(
        name='attack_screen', 
        button_names=['next_attack_button', 'end_battle_button'], 
        words=['tap', 'or', 'press', 'and', 'hold', 'to', 'deploy', 'troops', 'end', 'battle', 'available', 'loot']
    ),
    Screen(
        name='training_screen', 
        button_names=['quick_train_button', 'close_button'], 
        words=['train', 'troops', 'army', 'brew', 'spells', 'quick', 'train']
    ),
])


if __name__ == '__main__':
    window.show()

    screen = window.detect_screen()
    
    screenshot = window.screenshot(1)[0]
    screen.detect_buttons(screenshot)
    screen.show_buttons(screenshot)

    window.hide()