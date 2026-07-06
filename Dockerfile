FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
