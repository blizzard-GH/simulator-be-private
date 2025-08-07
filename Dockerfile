# FROM python:3.10-slim

# WORKDIR /app

# COPY requirements.txt ./
# RUN pip install -r requirements.txt

# COPY . .

# CMD [ "python", "./run.py" ]

# Use official Python image
FROM python:3.11-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Load environment variables (optional if handled by docker-compose)
# RUN pip install python-dotenv

# Expose your Flask app
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=127.0.0.1
ENV FLASK_RUN_PORT=5050

# Use gunicorn for production (instead of Flask dev server)
CMD ["gunicorn", "-b", "0.0.0.0:5050", "app:create_app()"]
