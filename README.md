# YOLOv5 + MLflow Microservices — an MLOps platform

A containerised, microservice-based MLOps application for image object detection.
A **YOLOv5** inference service exposes predictions over a REST API; an **MLflow**
service tracks the metrics and parameters of every run; **MongoDB** persists the
prediction and metrics data. The stack runs locally with **Docker Compose** and
deploys to **Kubernetes** (Minikube) through a single launch script.

## Architecture

| Service | Role | Port |
|---------|------|------|
| **YOLO service** | FastAPI service that runs YOLOv5 object detection/classification on uploaded images and logs each run's metrics. | `8000` |
| **MLflow service** | FastAPI + MLflow tracking server; records metrics and parameters for every experiment. | `8001` |
| **MongoDB** | Stores logs and metrics for both services. | internal |

- **Containerisation** — each service ships with its own `Dockerfile`; `docker-compose.yml` orchestrates the three for local development.
- **Kubernetes** — `k8s/` holds the namespace, deployments, services and ingress used to run the platform on a cluster.
- **One-command deploy** — `deploy_application.launch` provisions a fresh Linux host (Docker, kubectl, Minikube), builds the images inside Minikube's Docker daemon, and applies all Kubernetes resources.

## Repository layout

```
.
├── yolo-service/         # FastAPI YOLOv5 inference microservice
│   └── app/              #   routes (inference, metrics), models, config, weights
├── mlflow-service/       # FastAPI + MLflow experiment-tracking microservice
│   └── mlruns/           #   sample tracked runs (metrics / params / tags)
├── k8s/                  # Kubernetes manifests (namespace, deployments, services, ingress)
├── docker-compose.yml    # local orchestration of all three services
├── deploy_application.launch   # end-to-end Minikube deployment script
└── archive/              # earlier single-service prototype
```

## Running locally (Docker Compose)

```bash
docker compose up --build
# YOLO service   -> http://localhost:8000
# MLflow service -> http://localhost:8001
```

## Deploying to Kubernetes (Minikube)

```bash
chmod +x deploy_application.launch
./deploy_application.launch
```

The script installs Docker, kubectl and Minikube, starts the cluster, builds the
YOLO and MLflow images inside Minikube's Docker environment, applies the manifests
in `k8s/`, and prints the service endpoints. With Minikube running, the services are
reachable at `http://<minikube-ip>:8000` (YOLO) and `http://<minikube-ip>:8001`
(MLflow); MongoDB is internal to the cluster.

## Tech stack

Python · FastAPI · YOLOv5 (Ultralytics) · MLflow · MongoDB · Docker · Docker Compose · Kubernetes (Minikube)
