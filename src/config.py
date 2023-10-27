from enum import Enum


REFERENCE_SCREEN_SIZE = (1920, 1080)
SCREENSHOT_OUTER_BORDER: int = 10
SCREENSHOT_HEADER_SIZE: int = 32

TEMPLATES_DIR = "assets/templates"


class Model(Enum):
    BackBeat = (
        "BackBeat"  # Tesseract OCR model trained on BackBeat light font (smaller text)
    )
    SupercellMagic = (
        "SupercellMagic"  # Tesseract OCR model trained on Clash of Clans font
    )
    Eng = "eng"
