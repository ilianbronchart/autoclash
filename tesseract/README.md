# tesseract_tutorial

Credit to https://youtu.be/KE4xEzFGSU8 for the tutorial

# Fonts

CCBackBeatW00-Light Ultra-Light.ttf
Supercell-Magic.ttf

# Installation

Make sure to install the fonts in `./fonts` onto your system.

# Commands

Split BackBeat training data:

```
python3 main.py --split --font="CCBackBeatW00-Light Ultra-Light" --name=BackBeat -n 10000
```

Split SupercellMagic training data:

```
python3 main.py --split --font="Supercell-Magic" --name=SupercellMagic -n 10000
```
