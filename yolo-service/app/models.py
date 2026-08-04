from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class PredictionRequest(BaseModel):
    """Model for incoming prediction requests."""
    file: bytes  # Incoming image file as bytes (FastAPI automatically handles file uploads)

class PredictionResult(BaseModel):
    """Model for the response returned by YOLO inference."""
    class_name: str = Field(..., description="Name of the detected class")
    confidence: float = Field(..., description="Confidence score of the detection")

class PredictionResponse(BaseModel):
    """Model for the full prediction response."""
    predictions: List[PredictionResult]
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the prediction")
