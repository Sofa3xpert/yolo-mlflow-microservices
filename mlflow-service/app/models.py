from pydantic import BaseModel, Field
from typing import Optional

class LogMetricsRequest(BaseModel):
    """Model for incoming metric logging requests."""
    weights: str = Field(..., description="Name or path of the model weights used")
    confidence_threshold: float = Field(..., description="Confidence threshold used during inference")
    num_classes_predicted: int = Field(..., description="Number of unique classes predicted in the image")
    avg_confidence: float = Field(..., description="Average confidence score of the predictions")

class LogMetricsResponse(BaseModel):
    """Model for the response after logging metrics to MLFlow."""
    status: str = Field(..., description="Status of the logging operation")
    run_id: Optional[str] = Field(None, description="ID of the MLFlow run if successful")
