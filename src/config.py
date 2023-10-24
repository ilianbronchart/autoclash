REFERENCE_SCREEN_SIZE = (1679, 944)
SCREENSHOT_OUTER_BORDER = 10
SCREENSHOT_HEADER_SIZE = 32
WINDOW_OFFSET_TOP = 31
WINDOW_OFFSET = 10
WINDOW_TITLE = 'Clash of Clans'
TEMPLATES_DIR = 'assets/templates'
OCR_SAMPLES = 5
OCR_WHITE_THRESHOLD = 220

SCREENS = {
    'disconnected_screen': {
        'words': [
            'anyone', 'there', 'you', 'have', 'been', 'disconnected', 'due', 'to', 'inactivity'
        ],
        'buttons': []
    },
    'multiplayer_screen': {
        'words': [
            'unranked', 'practice', 'single', 'player'
        ],
        'buttons': ['close_button', 'find_match_button']
    },
    'main_screen': {
        'words': [
            'attack', 'shop'
        ],
        'buttons': ['attack_button']
    },
    'attack_screen': {
        'words': [
            'tap', 'or', 'press', 'and', 'hold', 'to', 'deploy', 'troops', 'end', 'battle', 'available', 'loot'
        ],
        'buttons': []
    }
}

