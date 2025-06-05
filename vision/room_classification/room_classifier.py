# from inference_sdk import InferenceHTTPClient
# from collections import defaultdict

# # Initialize the client with the given API URL and key
# CLIENT = InferenceHTTPClient(
#     api_url="https://detect.roboflow.com",
#     api_key="JK9wn65MGvuYlDWxOtZl")

# # Room categorization based on object types
# room_categories = {
#     "Bedroom": ["Bed", "Bed Frame", "Closet", "Desk"],
#     "Living Room": ["Sofa", "TV", "Dining Table", "Desk"],
#     "Kitchen": ["Stove", "Oven", "Fridge", "Microwave", "Dish Washer", "Sink", "Exhaust Hood", "Faucet", "Cupboard"],
#     "Washroom": ["Bathtub", "Toilet", "Toilet Sink", "Water Cubicle", "Water Heater", "Washing Machine", "Sink", "Faucet"],
#     "General": ["Door", "Windowsill", "AC", "Exhaust Fan", "Thermo Ventilator"]
# }

# # Function to classify room based on detected objects
# def classify_room(detections):
#     room_counts = defaultdict(float)

#     # Count how many objects belong to each room type (weighted by confidence score)
#     for detection in detections:
#         obj_class = detection.get("class", "Unknown")
#         confidence = detection.get("confidence", 0)  # Get confidence score
        
#         for room, objects in room_categories.items():
#             if obj_class in objects:
#                 room_counts[room] += confidence  # Add confidence as weight

#     # If no room is detected, return "Unknown"
#     if not room_counts:
#         return "Unknown", {}

#     # Find the room with the highest probability
#     most_probable_room = max(room_counts, key=room_counts.get)

#     return most_probable_room, room_counts

# # Perform inference on a local image
# image_path = r"C:\Users\hasin\OneDrive\Desktop\property_images_final\property_1\image_3.jpg"    # Replace with your image file path
# result = CLIENT.infer(image_path, model_id="all_finalize/3")

# # Extract detections
# detections = result.get("predictions", [])

# # Predict the room type
# predicted_room, probabilities = classify_room(detections)

# # Print detailed results
# print("\nDetected Objects:")
# for detection in detections:
#     obj_class = detection.get("class", "Unknown")
#     confidence = detection.get("confidence", 0) * 100  # Convert to percentage
#     print(f"- Object: {obj_class}, Confidence: {confidence:.2f}%")

# print("\nRoom Probabilities:")
# for room, score in probabilities.items():
#     print(f"{room}: {score:.2f}")

# print("\nPredicted Room Type:", predicted_room)



import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from collections import defaultdict
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ----- Step 1: Load model and processor -----
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model.eval()

# ----- Step 2: Define room categories -----
room_categories = {
    "Bedroom": ["bed", "couch", "chair", "potted plant"],
    "Living Room": ["couch", "tv", "remote", "vase"],
    "Kitchen": ["microwave", "oven", "sink", "refrigerator", "bottle"],
    "Washroom": ["toilet", "sink", "towel", "toothbrush"],
    "General": ["book", "laptop", "clock", "scissors"]
}

# ----- Step 3: Load image -----
image_path = BASE_DIR / "data" / "raw" / "property_images_final" / "property_21" / "image_14.jpg"
image = Image.open(image_path).convert("RGB")

# ----- Step 4: Run inference -----
inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# ----- Step 5: Post-process results -----
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.7)[0]

# ----- Step 6: Collect detected objects -----
detected_objects = []
draw = ImageDraw.Draw(image)

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    class_name = model.config.id2label[label.item()]
    detected_objects.append({"class": class_name, "confidence": score.item()})
    
    box = [round(i, 2) for i in box.tolist()]
    draw.rectangle(box, outline="red", width=2)
    draw.text((box[0], box[1]), f"{class_name} {score:.2f}", fill="red")

# ----- Step 7: Room classification -----
def classify_room(detections):
    room_counts = defaultdict(float)
    for det in detections:
        obj_class = det["class"]
        confidence = det["confidence"]
        for room, objects in room_categories.items():
            if obj_class.lower() in [o.lower() for o in objects]:
                room_counts[room] += confidence
    if not room_counts:
        return "Unknown", {}
    return max(room_counts, key=room_counts.get), room_counts

predicted_room, probabilities = classify_room(detected_objects)

# ----- Step 8: Print and plot -----
print("\nDetected Objects:")
for d in detected_objects:
    print(f"- {d['class']} ({d['confidence']*100:.1f}%)")

print("\nRoom Probabilities:")
for room, score in probabilities.items():
    print(f"{room}: {score:.2f}")

print("\nPredicted Room Type:", predicted_room)

# Plot image with boxes
plt.figure(figsize=(12, 8))
plt.imshow(image)
plt.title(f"Detected Room: {predicted_room}")
plt.axis("off")
plt.show()