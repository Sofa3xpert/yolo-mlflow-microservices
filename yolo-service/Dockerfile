# Base Python image
FROM python:3.11.8

# Set working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements_yolo.txt .
RUN pip install --no-cache-dir -r requirements_yolo.txt

# Copy application code into the container
COPY ./app ./app

# Expose the port YOLO Service will run on
EXPOSE 8000

# Command to run the YOLO Service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
