import argparse
import subprocess
from split_training_text import split_training_text

TRAINING_TEXT_FILE = "langdata/eng.training_text"

def main():
    parser = argparse.ArgumentParser(
        description="This script facilitates the training process for Tesseract OCR. It provides options for splitting training text, training the model, and managing training data.",
        epilog="Example usage: python script.py --split --font 'FontName' --name 'ModelName' -n 10000 --train --iterations 1000",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument('--split', action='store_true', help='Split training text into individual files.\n')
    parser.add_argument("--font", type=str, help="Specify the font name used in training. Required if --split is used.\n")
    parser.add_argument("--name", type=str, help="Name of the model. This will be used to name output directories and files.\n")
    parser.add_argument("-n", type=int, help="Number of training examples to generate. Required if --split is used.\n")

    parser.add_argument('--train', action='store_true', help='Initiate the training process for the model.\n')
    parser.add_argument('--iterations', type=int, help='Set the number of training iterations. Required if --train is used.\n')

    args = parser.parse_args()

    if args.split:
        if args.font is None or args.name is None or args.n is None:
            parser.error("--split requires --font, --name, and -n.")
        model_name = args.name
        output_directory = f"tesstrain/data/{model_name}-ground-truth"
        num_examples = args.n
        split_training_text(args.font, model_name, TRAINING_TEXT_FILE, output_directory, num_examples)

    if args.train:
        if args.iterations is None:
            parser.error("--train requires --iterations.")
        
        # TESSDATA_PREFIX=../tessdata make training MODEL_NAME=BackBeat START_MODEL=eng TESSDATA=../tessdata MAX_ITERATIONS=100
        # cp tesstrain/data/BackBeat.traineddata /usr/share/tesseract-ocr/4.00/tessdata/BackBeat.traineddata


if __name__ == "__main__":
    main()