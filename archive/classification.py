import torch
from PIL import Image
import sys
import os


def load_model():
    """Load the YOLOv5 model."""
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
    return model


def predict(model, image_path):
    """Perform inference on an input image."""
    # Load the image
    img = Image.open(image_path).convert("RGB")
    # Perform inference
    results = model(img)
    # Process results
    predictions = results.pandas().xyxy[0]  # Convert to pandas DataFrame
    class_names = predictions['name'].tolist()
    confidences = predictions['confidence'].tolist()
    return list(zip(class_names, confidences))


if __name__ == "__main__":
    # Parse arguments
    if len(sys.argv) != 2:
        print("Usage: python run_yolov5.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    # Check if weights exist
    weights_path = os.path.join("../yolo-service/app/weights", "yolov5s.pt")
    if not os.path.exists(weights_path):
        print(f"Error: Weights file not found at {weights_path}")
        sys.exit(1)

    # Load model
    print("Loading model...")
    model = load_model()

    # Perform prediction
    print("Running inference...")
    results = predict(model, image_path)

    # Display results
    print("Predictions:")
    for class_name, confidence in results:
        print(f"Class: {class_name}, Confidence: {confidence:.2f}")
