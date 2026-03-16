FROM python:3.11-slim

# Install system dependencies if needed (pypdf is pure python, so usually not needed)
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .

# Adding the flag here ensures the build never stops for PEP 668
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

COPY . .

# The command to run your app (Example: FastAPI)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# FastAPI and Streamlit are started by docker-compose