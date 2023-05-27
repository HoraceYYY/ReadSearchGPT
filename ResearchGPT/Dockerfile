# Dockerfile

# Start from a base Python 3.10.3 image
FROM python:3.10.3-slim

# Set a directory for the application
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# The command to run when the container is started
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
