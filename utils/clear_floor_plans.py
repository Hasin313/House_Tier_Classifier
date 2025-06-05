import os
from PIL import Image
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def is_floorplan_image(image_path, white_thresh=0.80, edge_thresh=0.005, variance_thresh=30, unique_thresh=20):
    try:
        img = Image.open(image_path).convert('L')
        img = img.resize((256, 256))
        img_np = np.array(img)

        white_ratio = np.mean(img_np > 235)       # more relaxed
        edge_ratio = np.mean(img_np < 35)         # lower cutoff
        variance = np.var(img_np)
        unique_colors = len(np.unique(img_np))

        if (
            white_ratio > white_thresh and edge_ratio > edge_thresh or
            (variance < variance_thresh and unique_colors < unique_thresh)
        ):
            return True
        return False
    except Exception as e:
        print(f"Error in image {image_path}: {e}")
        return False




def delete_floorplans_in_folder(folder_path):
    deleted = 0
    checked = 0

    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(folder_path, file)
            checked += 1
            if is_floorplan_image(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                deleted += 1

    return checked, deleted

def run_on_all_properties(root_path):
    total_checked = 0
    total_deleted = 0

    # Numerically sort folder names like property_1, property_2, ..., property_999
    folder_names = [f for f in os.listdir(root_path)
                    if os.path.isdir(os.path.join(root_path, f)) and f.startswith('property_')]
    folder_names = sorted(folder_names, key=lambda x: int(x.split('_')[-1]) if x.split('_')[-1].isdigit() else float('inf'))

    for folder_name in folder_names:
        folder_path = os.path.join(root_path, folder_name)
        print(f"\nScanning {folder_name}...")
        checked, deleted = delete_floorplans_in_folder(folder_path)
        print(f"{folder_name}: Checked = {checked}, Deleted = {deleted}")
        total_checked += checked
        total_deleted += deleted

    print("\n=== SUMMARY ===")
    print(f"Total images checked: {total_checked}")
    print(f"Total floorplan images deleted: {total_deleted}")

# Run the script on your dataset
root_property_path = BASE_DIR / "data" / "raw" / "property_images_final"
run_on_all_properties(root_property_path)