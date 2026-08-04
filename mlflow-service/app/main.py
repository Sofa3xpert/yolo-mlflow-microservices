import mlflow
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI()

# MLFlow setup
mlflow.set_experiment("YOLOv5-Classification")

class LogMetricsRequest(BaseModel):
    weights: str
    confidence_threshold: float
    num_classes_predicted: int
    avg_confidence: float

@app.post("/log_metrics")
def log_metrics(request: LogMetricsRequest):
    try:
        with mlflow.start_run():
            mlflow.log_param("weights", request.weights)
            mlflow.log_param("confidence_threshold", request.confidence_threshold)
            mlflow.log_metric("num_classes_predicted", request.num_classes_predicted)
            mlflow.log_metric("avg_confidence", request.avg_confidence)
        return {"status": "Metrics logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging metrics: {e}")
