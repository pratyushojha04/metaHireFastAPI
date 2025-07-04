# Use Python 3.8 slim for a lightweight base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Java, Node.js, and C++
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    nodejs \
    npm \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Verify installations
RUN javac --version && java --version && node --version && g++ --version

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files
COPY main.py .
COPY services/ services/
COPY api/ api/
COPY models/ models/
COPY data/ data/
COPY .env .

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port (Railway assigns PORT dynamically)
EXPOSE ${PORT:-8000}

# Load environment variables from .env file
ENV PYTHONUNBUFFERED=1

# Command to start FastAPI server, using PORT from environment
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]