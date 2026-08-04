# Common tasks for the YOLO + MLflow microservices platform.

.PHONY: up down logs build deploy clean

# Local development (Docker Compose)
up:            ## Build and start all services locally
	docker compose up --build

down:          ## Stop and remove local containers
	docker compose down

logs:          ## Tail logs from the running services
	docker compose logs -f

build:         ## Build the service images without starting them
	docker compose build

# Kubernetes (Minikube)
deploy:        ## Provision Minikube and deploy the full stack
	chmod +x deploy_application.launch && ./deploy_application.launch

clean:         ## Delete the Kubernetes namespace and its resources
	kubectl delete -f k8s/namespace.yaml --ignore-not-found
