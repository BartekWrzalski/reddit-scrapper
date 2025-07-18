# Wybór lekkiego obrazu z Pythonem
FROM python:3.10-slim

# Ustawienie katalogu roboczego
WORKDIR /app

RUN pip install --no-cache-dir ariadne uvicorn protobuf grpcio grpcio-tools fastapi

# Kopiowanie plików
COPY /app /app
COPY schema.graphql /app/schema.graphql

# Domyślna komenda uruchamiająca serwer
CMD ["uvicorn", "ariadne_client:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
