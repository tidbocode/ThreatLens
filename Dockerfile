FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY main.py .

VOLUME ["/app/data", "/app/chroma_db"]

ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
