from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.models import PredictionResult
from datetime import datetime
from bson import ObjectId
import httpx
import yaml

# Initialize the router
router = APIRouter()

# Load configuration
with open("app/config.yaml", "r") as f:
    config = yaml.safe_load(f)

MLFLOW_SERVICE_URL = config.get("service_url", "http://mlflow-service:8001")


@router.post("/log_metrics")
async def log_metrics_to_db(predictions: list[PredictionResult], user_id: str, db=Depends(get_db)):
    """
    Log prediction metrics to MongoDB and optionally forward to MLFlow Service.

    Args:
        predictions (list[PredictionResult]): List of predictions with confidence scores.
        user_id (str): ID of the user making the predictions.
        db: MongoDB dependency.

    Returns:
        dict: Status of the operation.
    """
    try:
        # Prepare the log entry
        avg_confidence = sum(p.confidence for p in predictions) / len(predictions) if predictions else 0
        log_entry = {
            "user_id": ObjectId(user_id),
            "predictions": [p.dict() for p in predictions],
            "timestamp": datetime.utcnow(),
            "avg_confidence": avg_confidence
        }

        # Insert into MongoDB
        result = await db["prediction_metrics"].insert_one(log_entry)
        log_id = str(result.inserted_id)

        # Forward metrics to MLFlow Service
        async with httpx.AsyncClient() as client:
            mlflow_payload = {
                "weights": config["weights_path"],
                "confidence_threshold": config["confidence_threshold"],
                "num_classes_predicted": len(predictions),
                "avg_confidence": avg_confidence
            }
            mlflow_response = await client.post(f"{MLFLOW_SERVICE_URL}/log_metrics", json=mlflow_payload)

            if mlflow_response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to log metrics to MLFlow")

        return {"status": "success", "log_id": log_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging metrics: {str(e)}")


@router.get("/metrics/{user_id}")
async def get_user_metrics(user_id: str, db=Depends(get_db)):
    """
    Fetch all metrics logged for a specific user.

    Args:
        user_id (str): ID of the user.

    Returns:
        list: List of logged metrics for the user.
    """
    try:
        metrics = await db["prediction_metrics"].find({"user_id": ObjectId(user_id)}).to_list(100)
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching metrics: {str(e)}")
