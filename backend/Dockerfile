FROM python:3.11-slim

WORKDIR /app

# Copy requirements from root (outside backend folder)
COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend app code
COPY backend/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
