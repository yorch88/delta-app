FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Ensure Python can locate the backend module
ENV PYTHONPATH=/app

# Change to backend directory for Flask commands
WORKDIR /app/backend

# Expose the Flask port
EXPOSE 5000

# Command to start the app
CMD ["flask", "run", "--host=0.0.0.0"]
