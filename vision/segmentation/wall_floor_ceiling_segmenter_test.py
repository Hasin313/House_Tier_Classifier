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
image_path = r"C:\house hold objects detection model\train\images\Toilet-219-_jpg.rf.385c81b1b143856ac564f7d977254a5b.jpg"
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

print("Predicted class IDs:", np.unique(segmentation))

# ----- Step 5: Class IDs -----
wall_classes = {0}
floor_classes = {3}
ceiling_classes = {5}

# ----- Step 6: Create masks -----
wall_mask = np.isin(segmentation, list(wall_classes)).astype(np.uint8) * 255
floor_mask = np.isin(segmentation, list(floor_classes)).astype(np.uint8) * 255
ceiling_mask = np.isin(segmentation, list(ceiling_classes)).astype(np.uint8) * 255

# ----- Step 7: Overlay floor and wall on image -----
original_np = np.array(image).copy()
overlay = original_np.copy()

# Apply Blue to Floor
overlay[floor_mask == 255] = [0, 0, 255]

# Apply Red to Wall
overlay[wall_mask == 255] = [255, 0, 0]

# Apply Green to Ceiling
overlay[ceiling_mask == 255] = [0, 255, 0]

# Blend
blended = Image.fromarray((0.5 * original_np + 0.5 * overlay).astype(np.uint8))


# ----- Step 8: Show results -----
fig, axs = plt.subplots(1, 6, figsize=(36, 6))
axs[0].imshow(image)
axs[0].set_title("Original Image")

axs[1].imshow(wall_mask, cmap="gray")
axs[1].set_title("Wall Mask")

axs[2].imshow(floor_mask, cmap="gray")
axs[2].set_title("Floor Mask")

axs[3].imshow(ceiling_mask, cmap="gray")
axs[3].set_title("Ceiling Mask")

axs[4].imshow(overlay)
axs[4].set_title("Overlay (R=Wall, G=Ceiling, B=Floor)")

axs[5].imshow(blended)
axs[5].set_title("Blended Overlay")

for ax in axs:
    ax.axis("off")

plt.tight_layout()
plt.show()