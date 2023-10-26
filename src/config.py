from enum import Enum


REFERENCE_SCREEN_SIZE = (1679, 944)
SCREENSHOT_OUTER_BORDER: int = 10
SCREENSHOT_HEADER_SIZE: int = 32


TEMPLATES_DIR = 'assets/templates'

OCR_SAMPLES = 5
OCR_WHITE_THRESHOLD = 220

class Model(Enum):
    BackBeat = 'BackBeat'
    SupercellMagic = 'SupercellMagic'