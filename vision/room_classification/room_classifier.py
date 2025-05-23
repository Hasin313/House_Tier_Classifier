from inference_sdk import InferenceHTTPClient
from collections import defaultdict

# Initialize the client with the given API URL and key
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="JK9wn65MGvuYlDWxOtZl")

# Room categorization based on object types
room_categories = {
    "Bedroom": ["Bed", "Bed Frame", "Closet", "Desk"],
    "Living Room": ["Sofa", "TV", "Dining Table", "Desk"],
    "Kitchen": ["Stove", "Oven", "Fridge", "Microwave", "Dish Washer", "Sink", "Exhaust Hood", "Faucet", "Cupboard"],
    "Washroom": ["Bathtub", "Toilet", "Toilet Sink", "Water Cubicle", "Water Heater", "Washing Machine", "Sink", "Faucet"],
    "General": ["Door", "Windowsill", "AC", "Exhaust Fan", "Thermo Ventilator"]
}

# Function to classify room based on detected objects
def classify_room(detections):
    room_counts = defaultdict(float)

    # Count how many objects belong to each room type (weighted by confidence score)
    for detection in detections:
        obj_class = detection.get("class", "Unknown")
        confidence = detection.get("confidence", 0)  # Get confidence score
        
        for room, objects in room_categories.items():
            if obj_class in objects:
                room_counts[room] += confidence  # Add confidence as weight

    # If no room is detected, return "Unknown"
    if not room_counts:
        return "Unknown", {}

    # Find the room with the highest probability
    most_probable_room = max(room_counts, key=room_counts.get)

    return most_probable_room, room_counts

# Perform inference on a local image
image_path = r"C:\Users\hasin\Downloads\SE_HouseImages\f7d725e19bc12182378180ab03264b6d-p_d.jpg"    # Replace with your image file path
result = CLIENT.infer(image_path, model_id="all_finalize/3")

# Extract detections
detections = result.get("predictions", [])

# Predict the room type
predicted_room, probabilities = classify_room(detections)

# Print detailed results
print("\nDetected Objects:")
for detection in detections:
    obj_class = detection.get("class", "Unknown")
    confidence = detection.get("confidence", 0) * 100  # Convert to percentage
    print(f"- Object: {obj_class}, Confidence: {confidence:.2f}%")

print("\nRoom Probabilities:")
for room, score in probabilities.items():
    print(f"{room}: {score:.2f}")

print("\nPredicted Room Type:", predicted_room)