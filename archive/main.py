import os
import yaml
import mlflow
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
from ultralytics import YOLO

# Load configuration from YAML file
with open('../yolo-service/app/config.yaml', "r") as f:
    config = yaml.safe_load(f)

# Load variables from configuration
WEIGHTS_PATH = config["weights_path"]
CONFIDENCE_THRESHOLD = config["confidence_threshold"]
MLFLOW_TRACKING_URI = config["mlflow_tracking_uri"]

# Set up MLFlow
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("YOLOv5-Classification")

# Initialize FastAPI
app = FastAPI()

# Load the YOLO model using ultralytics package
model = YOLO(WEIGHTS_PATH)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not model:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    try:
        # Read and process the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # Perform inference
        results = model(image)
        predictions = results[0].boxes  # Extract prediction boxes

        # Extract class names and confidences
        response = []
        for box in predictions:
            response.append({"class": model.names[int(box.cls.item())], "confidence": float(box.conf.item())})

        # Log metrics to MLFlow
        with mlflow.start_run():
            mlflow.log_param("weights", WEIGHTS_PATH)
            mlflow.log_param("confidence_threshold", CONFIDENCE_THRESHOLD)
            mlflow.log_metric("num_classes_predicted", len(response))
            if response:
                avg_confidence = sum([r["confidence"] for r in response]) / len(response)
                mlflow.log_metric("avg_confidence", avg_confidence)

        return {"predictions": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {e}")
