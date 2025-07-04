# Use Python 3.9 slim for compatibility with pandas==2.2.2
FROM python:3.9-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies with retries
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk \
    nodejs \
    npm \
    g++ \
    && rm -rf /var/lib/apt/lists/* || \
    (sleep 5 && apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk \
    nodejs \
    npm \
    g++ \
    && rm -rf /var/lib/apt/lists/*)

# Verify installations
RUN javac --version && java --version && node --version && g++ --version

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || \
    (sleep 5 && pip install --no-cache-dir -r requirements.txt)

# Copy only necessary files
COPY main.py .
COPY services/ services/
COPY api/ api/
COPY models/ models/
COPY data/ data/

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose dynamic port for Railway
EXPOSE ${PORT:-8000}

# Ensure logs are streamed
ENV PYTHONUNBUFFERED=1

# Healthcheck for Railway
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000} || exit 1

# Start FastAPI server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]