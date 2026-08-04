# YOLO Service

YOLO Service is a FastAPI-based microservice that performs image classification using the YOLOv5 model. It also logs metrics to MLFlow and MongoDB for further analysis.

## Features

- Predict classes and confidence scores for objects in an image.
- Log prediction metrics to MongoDB and MLFlow.

## Requirements

- Docker
- MongoDB
- MLFlow

## Endpoints

### `/predict` (POST)
- **Description:** Accepts an image file and returns predictions.
- **Request:**
  ```bash
  curl -X POST "http://localhost:8000/predict" \
       -H "Content-Type: multipart/form-data" \
       -F "file=@path/to/image.jpg"
  
### `/status` (GET)
- **Description:** Health check endpoint to verify if the service is running.
- **Request:**
  ```bash
  curl -X GET "http://localhost:8000/status"
  
### `/version` (GET)
- **Description:**  Returns the service name and version.
- **Request:**
  ```bash
  curl -X GET "http://localhost:8000/version"
