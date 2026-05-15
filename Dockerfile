FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY main.py .
COPY dashboard.py .

VOLUME ["/app/data", "/app/chroma_db"]
EXPOSE 8501

ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
