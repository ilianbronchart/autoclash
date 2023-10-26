import os
import random
import pathlib
import subprocess
import shutil
import time
from multiprocessing import Pool
from tqdm import tqdm


def create_dirs(output_directory):
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)

    os.makedirs(output_directory, exist_ok=True)


def get_lines(training_text_file, count=None):
    lines = []

    with open(training_text_file, "r", encoding="utf-8") as input_file:
        for line in input_file.readlines():
            lines.append(line.strip())

    random.shuffle(lines)
    if count:
        lines = lines[:count]

    return lines


def process_line(args):
    line_count, line, training_text_file, output_directory, font = args
    training_text_file_name = pathlib.Path(training_text_file).stem
    line_training_text = os.path.join(
        output_directory, f"{training_text_file_name}_{line_count}.gt.txt"
    )
    with open(line_training_text, "w", encoding="utf-8") as output_file:
        output_file.writelines([line])

    file_base_name = f"eng_{line_count}"

    subprocess.run(
        [
            "text2image",
            f"--font={font}",
            "--fonts_dir=fonts",
            f"--text={line_training_text}",
            f"--outputbase={output_directory}/{file_base_name}",
            "--max_pages=1",
            "--strip_unrenderable_words",
            "--leading=32",
            "--xsize=3200",
            "--ysize=250",
            "--char_spacing=1.0",
            "--exposure=0",
            "--unicharset_file=langdata/eng.unicharset",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def split_training_text(font, model_name, training_text_file, output_directory, num_examples):
    create_dirs(output_directory)
    lines = get_lines(training_text_file, num_examples)

    with Pool() as pool:
        args = [
            (i, line, training_text_file, output_directory, font)
            for i, line in enumerate(lines)
        ]
        for _ in tqdm(pool.imap_unordered(process_line, args), total=len(args)):
            pass
