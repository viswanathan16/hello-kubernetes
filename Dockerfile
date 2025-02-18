FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV IMAGE_VERSION="1.0.0"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

