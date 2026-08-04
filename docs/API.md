# API reference

Two FastAPI services expose REST endpoints. Interactive OpenAPI docs are served
by FastAPI at `/docs` on each service.

## YOLO service — `http://localhost:8000`

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/health` | Liveness check. |
| `POST` | `/predict` | Run YOLOv5 object detection on an uploaded image. Accepts `multipart/form-data` with an image `file`; returns detected classes, confidences and bounding boxes, and logs the run's metrics. |
| `GET`  | `/metrics` | Recent prediction metrics recorded for the service. |

Example:

```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@yolo-service/cat.jpeg"
```

## MLflow service — `http://localhost:8001`

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/health` | Liveness check. |
| `POST` | `/log` | Log metrics and parameters for an experiment run to MLflow (backed by MongoDB). |

Both services read their configuration from `app/config.yaml`. In the Kubernetes
deployment the same endpoints are reachable at `http://<minikube-ip>:8000` and
`http://<minikube-ip>:8001`; MongoDB is internal to the cluster.
