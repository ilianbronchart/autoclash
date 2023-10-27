import os
from multiprocessing import Pool
from tqdm import tqdm


def check_set(args):
    output_directory, i = args
    base_filename = f"eng_{i}"
    box_file = f"{base_filename}.box"
    gt_txt_file = f"{base_filename}.gt.txt"
    tif_file = f"{base_filename}.tif"

    box_path = os.path.join(output_directory, box_file)
    gt_txt_path = os.path.join(output_directory, gt_txt_file)
    tif_path = os.path.join(output_directory, tif_file)

    if not (
        os.path.exists(box_path)
        and os.path.exists(gt_txt_path)
        and os.path.exists(tif_path)
    ):
        return i
    return None


def find_incomplete_sets(output_directory, count):
    args = [(output_directory, i) for i in range(count)]

    incomplete_sets = set()
    with Pool() as pool:
        for result in tqdm(pool.imap_unordered(check_set, args), total=count):
            if result is not None:
                incomplete_sets.add(result)

    return incomplete_sets


def delete_files(args):
    output_directory, base_filename = args
    for ext in [".box", ".gt.txt", ".tif"]:
        file_path = os.path.join(output_directory, f"{base_filename}{ext}")
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return f"Deleted: {file_path}"
        except Exception as e:
            return f"Error deleting {file_path}: {e}"
    return None


def clean_training_data(model_name, output_directory, num_examples):
    print("Finding incomplete sets...")
    incomplete_sets = find_incomplete_sets(output_directory, num_examples)
    if not incomplete_sets:
        print("All files are part of complete sets.")
        return

    print(f"Found {len(incomplete_sets)} incomplete sets. Deleting related files...")

    args = [(output_directory, f"eng_{i}") for i in incomplete_sets]
    with Pool() as pool:
        for result in tqdm(pool.imap_unordered(delete_files, args), total=len(args)):
            if result:
                print(result)
