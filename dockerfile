# Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app


# Environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Copy the rest of the project
COPY . .

# Create directory for cache (if needed)
RUN mkdir -p cache

# Expose the port Flask uses
EXPOSE 5000

# Health check to ensure container is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:5000/ || exit 1


# Command to run the app
CMD ["python", "app.py"]
