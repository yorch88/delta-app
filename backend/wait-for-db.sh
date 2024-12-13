#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

cd /app/backend  # Ensure working directory is set to /app/backend

until pg_isready -h "$host" -p 5432 > /dev/null 2>&1; do
  echo "Waiting for database to be ready..."
  sleep 1
done

echo "Database is ready. Checking migrations..."

# Initialize migrations folder if missing
if [ ! -d "migrations" ]; then
  echo "Initializing migrations folder..."
  flask db init
fi

echo "Applying migrations..."
flask db migrate -m "Auto migration"
flask db upgrade

exec $cmd
