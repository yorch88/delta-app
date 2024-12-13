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
	docker exec -it $(BACKEND_SERVICE) bash
#docker exec -it $(BACKEND_SERVICE) /bin/sh

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

db-migrate-all:
	docker exec -it $(BACKEND_SERVICE) bash -c "\
	if [ ! -d 'migrations' ]; then flask db init; fi && \
	flask db migrate -m \"$(msg)\" && \
	flask db upgrade"

db-migrate:
	docker exec -it $(BACKEND_SERVICE) flask db migrate

db-upgrade:
	docker exec -it $(BACKEND_SERVICE) flask db upgrade

db-stamp:
	docker exec -it $(BACKEND_SERVICE) bash -c "\
	if [ ! -d 'migrations' ]; then flask db init; fi && \
	flask db migrate -m \"$(msg)\" && \
	flask db stamp head"

db-stampc:
	docker exec -it $(BACKEND_SERVICE) flask db stamp head

fix-migrations:
	@echo "Clearing Alembic version table..."
	docker exec -it $(DB_SERVICE) psql -U myuser -d delta-db -c "DELETE FROM alembic_version;"

# Recreate migrations and apply them
recreate-migrations:
	@echo "Generating and applying new migrations..."
	docker exec -it $(BACKEND_SERVICE) flask db migrate -m "Recreated migrations"
	docker exec -it $(BACKEND_SERVICE) flask db upgrade

# 1. Backup Database (customize this as necessary)
db-backup:
	@echo "Backing up database..."
	docker exec -t $(DB_SERVICE) pg_dump -U myuser -F c delta-db > backup/delta-db-backup.sql

# 2. Clear Alembic Version Table (to reset migration history)
clear-alembic-version:
	@echo "Clearing Alembic version table..."
	docker exec -it $(DB_SERVICE) psql -U myuser -d delta-db -c "DELETE FROM alembic_version;"

# 3. Generate New Migration
generate-migration:
	@echo "Generating new migration..."
	docker exec -it $(BACKEND_SERVICE) flask db migrate -m "Recreated migrations"

# 4. Apply Migrations
apply-migration:
	@echo "Applying migrations..."
	docker exec -it $(BACKEND_SERVICE) flask db upgrade

# 5. Run All Steps (run backup, clear alembic, generate migration, and apply migration in one go)
migrate-db: db-backup clear-alembic-version generate-migration apply-migration
	@echo "Database backup, migration creation, and upgrade complete!"

run-update-db:
	docker exec -it $(BACKEND_SERVICE) python migrations/script_update.py


run-flask-upgrade:
	docker exec -it $(BACKEND_SERVICE) flask db upgrade $(MIGRATION_ID)

#example how run: make run-flask-upgrade MIGRATION_ID=b1ed94efa472
run-flask-downgrade:
	docker exec -it $(BACKEND_SERVICE) flask db downgrade $(MIGRATION_ID)

#example: make run-update-column MIGRATION_MSG="Add column with nullable True"
run-update-column:
	docker exec -it $(BACKEND_SERVICE)  flask db migrate -m "$(MIGRATION_MSG)"
	docker exec -it $(BACKEND_SERVICE)  flask db upgrade
	docker exec -it $(BACKEND_SERVICE)  python migrations/script_update.py
