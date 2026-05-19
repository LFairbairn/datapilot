FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir streamlit httpx mcp[cli] pandas plotly

COPY src/ ./src/

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
