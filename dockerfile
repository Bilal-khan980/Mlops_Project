# Backend Dockerfile
FROM python:3.11-slim
# Set working directory
WORKDIR /app
# Copy the application code
COPY . /app
# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Expose the backend service port
EXPOSE 8000
# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]