FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if needed (none required for PyMySQL)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 5000
EXPOSE 5000

# Run the application with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]