from pathlib import Path
import streamlit as st
import os
from PIL import Image
import pandas as pd

# BASE_DIR = repo root, assuming script is in utils/
BASE_DIR = Path(__file__).resolve().parent.parent

segmented_floor_path = BASE_DIR / "data" / "processed" / "wall_floor_ceiling_segmented_images" / "floor"
original_images_root = BASE_DIR / "data" / "raw" / "property_images_final"
label_csv_path = BASE_DIR / "data" / "labels_floor.csv"

if label_csv_path.exists():
    label_df = pd.read_csv(label_csv_path)
else:
    label_df = pd.DataFrame(columns=["image_name", "score", "confidence"])

all_floor_images = sorted([f for f in os.listdir(segmented_floor_path) if f.endswith('.png')])

# Filter already labeled
labeled_images = set(label_df["image_name"].tolist())
unlabeled_images = [f for f in all_floor_images if f not in labeled_images]

# Sidebar: score counts
with st.sidebar:
    st.header("📊 Labeled Score Counts")
    score_counts = label_df['score'].value_counts().reindex(range(1, 11), fill_value=0)
    for score, count in score_counts.items():
        st.write(f"Score {score}: {count}")

# Main UI
st.title("🏠 Floor Scoring Tool")
st.markdown("Label the condition of the floor based on the segmented image and its original counterpart.")
st.info(f"Labeled: {len(labeled_images)} / {len(all_floor_images)} | Remaining: {len(unlabeled_images)}")

# Stop if nothing to label
if not unlabeled_images:
    st.success("🎉 All images labeled!")
    st.stop()

# Pick one image
current_image = unlabeled_images[0]

# Parse original image path
parts = current_image.split("_")
property_id = parts[1]
image_id = parts[3]
original_image_name = f"image_{image_id}.jpg"
original_image_path = os.path.join(original_images_root, f"property_{property_id}", original_image_name)
segmented_image_path = os.path.join(segmented_floor_path, current_image)

# Display images
# Display images
col1, col2 = st.columns(2)
with col1:
    st.image(Image.open(original_image_path), caption="Original Image", use_container_width=True)
with col2:
    st.image(Image.open(segmented_image_path), caption="Segmented Floor", use_container_width=True)

# Labeling UI
st.subheader("Give Score (1-10)")
score = st.radio("Select a score:", list(range(1, 11)), horizontal=True, key="score")

st.subheader("Confidence Level")
confidence = st.radio("Select confidence:", ["Low", "Medium", "High"], horizontal=True, key="confidence")

if st.button("Submit Label"):
    new_row = {"image_name": current_image, "score": score, "confidence": confidence}
    label_df = pd.concat([label_df, pd.DataFrame([new_row])], ignore_index=True)
    label_df.to_csv(label_csv_path, index=False)
    st.success("Label submitted successfully!")
    st.rerun()