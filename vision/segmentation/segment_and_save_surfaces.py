# import os
# import numpy as np
# from PIL import Image
# from pathlib import Path
# import logging
# from wall_floor_ceiling_segmenter_final import segment_image  # Import your segmentation function

# # Setup logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# def has_valid_masks(wall_mask, floor_mask, ceiling_mask):
#     """Check if any of the masks contain non-zero pixels"""
#     if wall_mask is None or floor_mask is None or ceiling_mask is None:
#         return False
#     return np.any(wall_mask > 0) or np.any(floor_mask > 0) or np.any(ceiling_mask > 0)

# def create_masked_image(original_image, mask):
#     """Create an image where only the masked area is visible (rest blacked out)"""
#     original_np = np.array(original_image)
#     masked_image = original_np.copy()
    
#     # Black out areas where mask is 0
#     mask_3channel = np.stack([mask, mask, mask], axis=2) / 255.0
#     masked_image = (masked_image * mask_3channel).astype(np.uint8)
    
#     return Image.fromarray(masked_image)

# def save_segmented_surfaces(original_image, wall_mask, floor_mask, ceiling_mask, 
#                           output_property_dir, image_name_base):
#     """Save the original image and masked surface images"""
    
#     # Create subdirectories
#     subdirs = ['original', 'wall', 'floor', 'ceiling']
#     for subdir in subdirs:
#         os.makedirs(os.path.join(output_property_dir, subdir), exist_ok=True)
    
#     # Save original image
#     original_path = os.path.join(output_property_dir, 'original', f"{image_name_base}.png")
#     original_image.save(original_path)
    
#     # Save masked surfaces (only if they have content)
#     masks_and_names = [
#         (wall_mask, 'wall'),
#         (floor_mask, 'floor'),
#         (ceiling_mask, 'ceiling')
#     ]
    
#     saved_surfaces = []
#     for mask, surface_name in masks_and_names:
#         if np.any(mask > 0):  # Only save if mask has content
#             masked_image = create_masked_image(original_image, mask)
#             surface_path = os.path.join(
#                 output_property_dir, 
#                 surface_name, 
#                 f"{image_name_base}_{surface_name}.png"
#             )
#             masked_image.save(surface_path)
#             saved_surfaces.append(surface_name)
    
#     return saved_surfaces

# def get_image_files(directory):
#     """Get all image files from a directory"""
#     image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
#     image_files = []
    
#     for file in os.listdir(directory):
#         if Path(file).suffix.lower() in image_extensions:
#             image_files.append(file)
    
#     return sorted(image_files)

# def process_images():
#     """Main processing function"""

#     input_dir = r"C:\Users\hasin\OneDrive\Desktop\House_Tier_Classifier\data\raw\property_images_final"
#     output_dir = r"C:\Users\hasin\OneDrive\Desktop\House_Tier_Classifier\data\processed\wall_floor_ceiling_segmented_images"

    
#     # Check if input directory exists
#     if not os.path.exists(input_dir):
#         logger.error(f"Input directory '{input_dir}' not found!")
#         return
    
#     # Create output directory
#     os.makedirs(output_dir, exist_ok=True)
    
#     # # Get all property folders
#     # property_folders = [f for f in os.listdir(input_dir) 
#     #                    if os.path.isdir(os.path.join(input_dir, f)) and f.startswith('property_')]
    
#     # Get all property folders
#     property_folders = [f for f in os.listdir(input_dir) 
#                         if os.path.isdir(os.path.join(input_dir, f)) and f.startswith('property_')]

#     # Sort them numerically by their ID
#     property_folders = sorted(
#         property_folders,
#         key=lambda x: int(x.split('_')[-1]) if x.split('_')[-1].isdigit() else float('inf')
#     )

    
#     if not property_folders:
#         logger.error("No property folders found!")
#         return
    
#     logger.info(f"Found {len(property_folders)} property folders")
    
#     total_processed = 0
#     total_skipped = 0
    
#     # Process each property folder
#     for property_folder in sorted(property_folders):
#         property_input_dir = os.path.join(input_dir, property_folder)
#         property_output_dir = os.path.join(output_dir, property_folder)
        
#         logger.info(f"Processing {property_folder}...")
        
#         # Get all image files in this property folder
#         image_files = get_image_files(property_input_dir)
        
#         if not image_files:
#             logger.warning(f"No image files found in {property_folder}")
#             continue
        
#         property_processed = 0
#         property_skipped = 0
        
#         # Process each image
#         for image_file in image_files:
#             image_path = os.path.join(property_input_dir, image_file)
#             image_name_base = Path(image_file).stem
            
#             try:
#                 # Run segmentation
#                 original_image, wall_mask, floor_mask, ceiling_mask = segment_image(image_path)
                
#                 # Check if any masks have content
#                 if not has_valid_masks(wall_mask, floor_mask, ceiling_mask):
#                     logger.info(f"  Skipping {image_file} - no interior surfaces detected")
#                     property_skipped += 1
#                     continue
                
#                 # Save segmented surfaces
#                 saved_surfaces = save_segmented_surfaces(
#                     original_image, wall_mask, floor_mask, ceiling_mask,
#                     property_output_dir, image_name_base
#                 )
                
#                 logger.info(f"  Processed {image_file} - saved surfaces: {', '.join(saved_surfaces)}")
#                 property_processed += 1
                
#             except Exception as e:
#                 logger.error(f"  Error processing {image_file}: {str(e)}")
#                 property_skipped += 1
        
#         logger.info(f"  {property_folder}: {property_processed} processed, {property_skipped} skipped")
#         total_processed += property_processed
#         total_skipped += property_skipped
    
#     logger.info(f"COMPLETE: {total_processed} images processed, {total_skipped} skipped")

# if __name__ == "__main__":
#     logger.info("Starting batch image segmentation processing...")
#     process_images()
#     logger.info("Processing complete!")


import os
import numpy as np
from PIL import Image
from pathlib import Path
import logging
from wall_floor_ceiling_segmenter_final import segment_image  # Import your segmentation function


BASE_DIR = Path(__file__).resolve().parent.parent

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def has_valid_masks(wall_mask, floor_mask, ceiling_mask):
    """Check if any of the masks contain non-zero pixels"""
    if wall_mask is None or floor_mask is None or ceiling_mask is None:
        return False
    return np.any(wall_mask > 0) or np.any(floor_mask > 0) or np.any(ceiling_mask > 0)

def create_masked_image(original_image, mask):
    """Create an image where only the masked area is visible (rest blacked out)"""
    original_np = np.array(original_image)
    masked_image = original_np.copy()
    
    # Black out areas where mask is 0
    mask_3channel = np.stack([mask, mask, mask], axis=2) / 255.0
    masked_image = (masked_image * mask_3channel).astype(np.uint8)
    
    return Image.fromarray(masked_image)

def save_segmented_surfaces(original_image, wall_mask, floor_mask, ceiling_mask, 
                          output_base_dir, property_name, image_name_base):
    """Save the masked surface images in flat structure"""
    
    # Create surface directories at the base level
    surface_dirs = ['wall', 'floor', 'ceiling']
    for surface_dir in surface_dirs:
        # os.makedirs(os.path.join(output_base_dir, surface_dir), exist_ok=True)
        (output_base_dir / surface_dir).mkdir(parents=True, exist_ok=True)
    
    # Save masked surfaces (only if they have content)
    masks_and_names = [
        (wall_mask, 'wall'),
        (floor_mask, 'floor'),
        (ceiling_mask, 'ceiling')
    ]
    
    saved_surfaces = []
    for mask, surface_name in masks_and_names:
        if np.any(mask > 0):  # Only save if mask has content
            masked_image = create_masked_image(original_image, mask)
            
            # Create filename: property_X_image_Y_surface.png
            filename = f"{property_name}_{image_name_base}_{surface_name}.png"
            # surface_path = os.path.join(output_base_dir, surface_name, filename)

            surface_path = output_base_dir / surface_name / filename

            masked_image.save(surface_path)
            saved_surfaces.append(surface_name)
    
    return saved_surfaces

def get_image_files(directory):
    """Get all image files from a directory"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    image_files = []
    
    for file in os.listdir(directory):
        if Path(file).suffix.lower() in image_extensions:
            image_files.append(file)
    
    return sorted(image_files)

def process_images():
    """Main processing function"""

    input_dir = BASE_DIR / "data" / "raw" / "property_images_final"
    output_dir = BASE_DIR / "data" / "processed" / "wall_floor_ceiling_segmented_images"
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        logger.error(f"Input directory '{input_dir}' not found!")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all property folders
    # property_folders = [f for f in os.listdir(input_dir) 
    #                     if os.path.isdir(os.path.join(input_dir, f)) and f.startswith('property_')]

    property_folders = [f for f in input_dir.iterdir() if f.is_dir() and f.name.startswith('property_')]

    # Sort them numerically by their ID
    # property_folders = sorted(
    #     property_folders,
    #     key=lambda x: int(x.split('_')[-1]) if x.split('_')[-1].isdigit() else float('inf')
    # )
    property_folders = sorted(
        property_folders,
        key=lambda x: int(x.name.split('_')[-1]) if x.name.split('_')[-1].isdigit() else float('inf')
    )

    
    if not property_folders:
        logger.error("No property folders found!")
        return
    
    logger.info(f"Found {len(property_folders)} property folders")
    
    total_processed = 0
    total_skipped = 0
    
    # Process each property folder
    for property_folder in property_folders:
        # property_input_dir = os.path.join(input_dir, property_folder)
        property_input_dir = input_dir / property_folder
        
        logger.info(f"Processing {property_folder}...")
        
        # Get all image files in this property folder
        image_files = get_image_files(property_input_dir)
        
        if not image_files:
            logger.warning(f"No image files found in {property_folder}")
            continue
        
        property_processed = 0
        property_skipped = 0
        
        # Process each image
        for image_file in image_files:
            image_path = os.path.join(property_input_dir, image_file)
            image_name_base = Path(image_file).stem
            
            try:
                # Run segmentation
                original_image, wall_mask, floor_mask, ceiling_mask = segment_image(image_path)
                
                # Check if any masks have content
                if not has_valid_masks(wall_mask, floor_mask, ceiling_mask):
                    logger.info(f"  Skipping {image_file} - no interior surfaces detected")
                    property_skipped += 1
                    continue
                
                # Save segmented surfaces in flat structure
                saved_surfaces = save_segmented_surfaces(
                    original_image, wall_mask, floor_mask, ceiling_mask,
                    output_dir, property_folder, image_name_base
                )
                
                logger.info(f"  Processed {property_folder}/{image_file} - saved surfaces: {', '.join(saved_surfaces)}")
                property_processed += 1
                
            except Exception as e:
                logger.error(f"  Error processing {image_file}: {str(e)}")
                property_skipped += 1
        
        logger.info(f"  {property_folder}: {property_processed} processed, {property_skipped} skipped")
        total_processed += property_processed
        total_skipped += property_skipped
    
    logger.info(f"COMPLETE: {total_processed} images processed, {total_skipped} skipped")

if __name__ == "__main__":
    logger.info("Starting batch image segmentation processing...")
    process_images()
    logger.info("Processing complete!")