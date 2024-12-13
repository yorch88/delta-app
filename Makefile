# Define common variables
PROJECT_NAME := my_project
FRONTEND_SERVICE := flask_frontend_c
BACKEND_SERVICE := flask-backend
DB_SERVICE := postgres

# Define Docker Compose command
DOCKER_COMPOSE := docker-compose -f docker-compose.yml

# Build all services
build:
	$(DOCKER_COMPOSE) build

# Build frontend service
build-frontend:
	$(DOCKER_COMPOSE) build frontend

# Build backend service
build-backend:
	$(DOCKER_COMPOSE) build backend

# Build db service
build-db:
	$(DOCKER_COMPOSE) build db

# Start all services
up:
	$(DOCKER_COMPOSE) up -d

# Start all services and builds
upb:
	$(DOCKER_COMPOSE) up --build

# Start frontend service only
up-frontend:
	$(DOCKER_COMPOSE) up -d frontend
	$(DOCKER_COMPOSE) logs -f frontend

# Start backend service only
up-backend:
	$(DOCKER_COMPOSE) up -d backend

# Start backend service and postgres service
up-bp:
	$(DOCKER_COMPOSE) up backend db

# Start db service only
up-db:
	$(DOCKER_COMPOSE) up -d db

# Stop all services
down:
	$(DOCKER_COMPOSE) down

# Stop all services and volumes
downv:
	$(DOCKER_COMPOSE) down --volumes

# Stop frontend service only
down-frontend:
	$(DOCKER_COMPOSE) stop frontend

# Stop backend service only
down-backend:
	$(DOCKER_COMPOSE) stop backend

# Stop db service only
down-db:
	$(DOCKER_COMPOSE) stop db

# Access the frontend container CLI
exec-frontend:
	docker exec -it $(FRONTEND_SERVICE) /bin/sh

# Access the backend container CLI
exec-backend:
	docker exec -it $(BACKEND_SERVICE) /bin/sh

# Access the db container CLI
exec-db:
	docker exec -it $(DB_SERVICE) /bin/sh

# View logs for frontend service
logs-frontend:
	$(DOCKER_COMPOSE) logs -f frontend

# View logs for backend service
logs-backend:
	$(DOCKER_COMPOSE) logs -f backend

# View logs for db service
logs-db:
	$(DOCKER_COMPOSE) logs -f db

# View logs for all services
logs:
	$(DOCKER_COMPOSE) logs -f

# Clean up (Remove containers, networks, and volumes)
clean:
	$(DOCKER_COMPOSE) down -v --rmi all

