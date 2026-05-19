FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir mcp[cli] pandas uvicorn

COPY src/ ./src/

EXPOSE 8000

CMD ["python", "src/server.py"]
