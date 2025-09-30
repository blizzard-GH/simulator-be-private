# Use official Python image
FROM python:3.11-slim

# ---- Zscaler certificate fix ----
# Copy Zscaler cert into image
COPY zscaler_root.crt /usr/local/share/ca-certificates/zscaler_root.crt

# Install cert dependencies & update trust store
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates openssl \
 && update-ca-certificates || true \
 && rm -rf /var/lib/apt/lists/*

# Point Python + pip + requests to updated cert bundle
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
# --------------------------------

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
