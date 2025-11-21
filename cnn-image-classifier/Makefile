.PHONY: build up down logs restart clean dev-backend dev-frontend install-deps gpu-check

# Production
build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

restart:
	docker compose restart

clean:
	docker compose down -v --rmi all

# Development
dev-backend:
	cd backend && pip install -r requirements.txt && python -m app.main

dev-frontend:
	cd frontend && npm install && npm run dev

install-deps:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

# Training
train:
	cd backend && python train.py

train-docker:
	docker run --rm --gpus all --network host -v ./backend/app/ml_model/saved_models:/app/app/ml_model/saved_models cnn-image-classifier-backend python train.py

# GPU
gpu-check:
	docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi

# Help
help:
	@echo "Commands:"
	@echo "  make build        - Build Docker images"
	@echo "  make up           - Start containers"
	@echo "  make down         - Stop containers"
	@echo "  make logs         - View logs"
	@echo "  make restart      - Restart containers"
	@echo "  make clean        - Remove containers and images"
	@echo "  make dev-backend  - Run backend locally"
	@echo "  make dev-frontend - Run frontend locally"
	@echo "  make gpu-check    - Verify GPU access"
	@echo "  make train        - Train model locally"
	@echo "  make train-docker - Train model in Docker"
