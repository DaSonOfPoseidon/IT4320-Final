# Use an official Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Environment variables (optional but nice)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port Flask uses
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
