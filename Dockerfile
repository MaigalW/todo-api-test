# Using pyton 3.12 image
FROM python:3.12-slim

# The working directory will be inside the container
WORKDIR /code

# Copy proyect files to container
COPY . /code

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# FastAPI port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
