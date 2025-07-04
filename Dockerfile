# Use Python 3.8 slim as base image to keep size manageable
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Java, Node.js, C++, and other tools
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

# Copy project files
COPY . .

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port 8000
EXPOSE 8000

# Set environment variables (override with .env file)
ENV MONGO_URI="mongodb+srv://opratyush12:Ir3BVLKFr0lShShR@metahire.lwcazyx.mongodb.net/?retryWrites=true&w=majority"
ENV SCORING_METHOD=sbert
ENV MONGO_DB_NAME=interview_db
ENV LOG_LEVEL=INFO
ENV DATA_DIR=data
ENV PORT=8000

# Command to start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]