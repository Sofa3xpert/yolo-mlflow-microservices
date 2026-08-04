from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import io
from ultralytics import YOLO
import yaml

router = APIRouter()

# Load configuration
with open("app/config.yaml", "r") as f:
    config = yaml.safe_load(f)

model = YOLO(config["weights_path"])

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        results = model(image)
        response = [{"class": model.names[int(box.cls.item())], "confidence": float(box.conf.item())} for box in results[0].boxes]
        return {"predictions": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
