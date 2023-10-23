WINDOW_OFFSET_TOP = 31
WINDOW_OFFSET = 10
WINDOW_TITLE = 'Clash of Clans'
REFERENCE_IMAGES_DIR = 'assets/reference_images'
OCR_SAMPLES = 5
OCR_WHITE_THRESHOLD = 220

SCREEN_TEXT = {
    'disconnected_screen': {
        'include': [
            'anyone', 'there', 'you', 'have', 'been', 'disconnected', 'due', 'to', 'inactivity'
        ],
        'exclude': []
    },
    'multiplayer_screen': {
        'include': [
            'unranked', 'practice', 'single', 'player'
        ],
    },
    'main_screen': {
        'include': [
            'attack', 'shop'
        ],
    },
    'attack_screen': {
        'include': [
            'tap', 'or', 'press', 'and', 'hold', 'to', 'deploy', 'troops', 'end', 'battle', 'available', 'loot'
        ],
    }
}
