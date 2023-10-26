import os
import cv2
import pytesseract
from difflib import SequenceMatcher
from tqdm import tqdm
from PIL import Image, ImageOps


def load_ground_truth(text_file_path):
    with open(text_file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


def calculate_accuracy(ground_truth, ocr_result):
    matcher = SequenceMatcher(None, ground_truth, ocr_result)
    return matcher.ratio()


def test_model(model_path, test_images_dir):
    if not os.path.exists(model_path):
        print("Error: Model path does not exist.")
        return

    if not os.path.exists(test_images_dir):
        print("Error: Test images directory does not exist.")
        return

    image_files = [
        f
        for f in os.listdir(test_images_dir)
        if os.path.isfile(os.path.join(test_images_dir, f)) and f.endswith(".png")
    ]
    if not image_files:
        print("Error: No image files found in the specified directory.")
        return

    total_accuracy = 0
    print("Testing model...")

    for image_file in image_files:
        image_path = os.path.join(test_images_dir, image_file)
        # text_file_path = os.path.join(
        #     test_images_dir, os.path.splitext(image_file)[0] + ".txt"
        # )

        # if not os.path.exists(text_file_path):
        #     print(
        #         f"Warning: No ground truth text file found for image {image_file}. Skipping..."
        #     )
        #     continue

        image = Image.open(image_path).convert("L")  # Convert image to grayscale
        image = ImageOps.invert(image)
        # ground_truth = load_ground_truth(text_file_path)
        ocr_result = pytesseract.image_to_string(
            image, config=f"--psm 4 --oem 3 -l BackBeat"
        )

        print(ocr_result.replace("\n", ""))
        # accuracy = calculate_accuracy(ground_truth, ocr_result)
        # total_accuracy += accuracy
        # print(f"Accuracy for {image_file}: {accuracy * 100:.2f}%")

    # average_accuracy = total_accuracy / len(image_files)
    # print(f"Average accuracy: {average_accuracy * 100:.2f}%")


if __name__ == "__main__":
    model = "BackBeat"
    model_path = f"tesseract/tessdata"
    test_images_dir = f"test/{model}"
    test_model(model_path, test_images_dir)
