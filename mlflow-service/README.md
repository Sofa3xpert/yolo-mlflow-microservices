# MLFlow Service

MLFlow Service is a FastAPI-based microservice that handles logging and tracking of metrics and parameters for experiments.

## Features

- Log metrics and parameters for machine learning experiments.
- Expose metrics via the MLFlow UI.

## Requirements

- Docker
- MongoDB (optional)

## Endpoints

### `/log_metrics` (POST)
- **Description:** Logs metrics to MLFlow.
- **Request:**
  ```bash
  curl -X POST "http://localhost:8001/log_metrics" \
       -H "Content-Type: application/json" \
       -d '{
             "weights": "yolov5s.pt",
             "confidence_threshold": 0.5,
             "num_classes_predicted": 3,
             "avg_confidence": 0.87
           }'
