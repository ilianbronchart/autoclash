# autoclash

## Installation

### Python dependencies

Using PowerShell

```
cd \path\to\autoclash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip3 install -r requirements.txt
```

### Tesseract Optical Character Recognition

[Install Tesseract here](https://github.com/UB-Mannheim/tesseract/wiki)

Create a `.env` file in the root directory with the following contents:

```
TESSDATA_PATH=/path/to/tesseract/tessdata
```
