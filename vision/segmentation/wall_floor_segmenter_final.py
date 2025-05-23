import torch
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from transformers import SegformerImageProcessor, SegformerForSemanticSegmentation

# ----- Step 1: Load model and processor -----
model_name = "nvidia/segformer-b0-finetuned-ade-512-512"
processor = SegformerImageProcessor.from_pretrained(model_name)
model = SegformerForSemanticSegmentation.from_pretrained(model_name)
model.eval()

# ----- Step 2: Load image -----
image_path = r"C:\Users\hasin\Downloads\SE_HouseImages\9eed1c497936be846d626feb50016448-p_d.jpg"  # change to match your filename
image = Image.open(image_path).convert("RGB")
original_size = image.size  # (W, H)

# ----- Step 3: Preprocess & Predict -----
inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted = logits.argmax(dim=1)[0].cpu().numpy()

# ----- Step 4: Resize segmentation to original size -----
segmentation_resized = Image.fromarray(predicted.astype(np.uint8)).resize(original_size, resample=Image.NEAREST)
segmentation = np.array(segmentation_resized)

# ----- Step 5: Class IDs -----
wall_classes = {0}  # wall
floor_classes = {3}  # floor

# ----- Step 6: Create masks -----
wall_mask = np.isin(segmentation, list(wall_classes)).astype(np.uint8) * 255
floor_mask = np.isin(segmentation, list(floor_classes)).astype(np.uint8) * 255

# ----- Step 7: Overlay floor and wall on image -----
original_np = np.array(image).copy()
overlay = original_np.copy()

# Apply blue color for floor
overlay[floor_mask == 255] = [0, 0, 255]

# Apply red color for wall — note: applied *after* floor so it will appear on top if overlapping
overlay[wall_mask == 255] = [255, 0, 0]

# Blend original and overlay
blended = Image.fromarray((0.5 * original_np + 0.5 * overlay).astype(np.uint8))

# ----- Step 8: Show results -----
fig, axs = plt.subplots(1, 5, figsize=(30, 6))
axs[0].imshow(image)
axs[0].set_title("Original Image")
axs[1].imshow(wall_mask, cmap="gray")
axs[1].set_title("Wall Mask")
axs[2].imshow(floor_mask, cmap="gray")
axs[2].set_title("Floor Mask")
axs[3].imshow(overlay)
axs[3].set_title("Overlay (Pure Colors)")
axs[4].imshow(blended)
axs[4].set_title("Blended Overlay (Red=Wall, Blue=Floor)")

for ax in axs:
    ax.axis("off")
plt.tight_layout()
plt.show()