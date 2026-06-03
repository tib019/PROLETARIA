FROM python:3.11-slim
WORKDIR /app
COPY serve.py .
RUN pip install fastapi uvicorn requests
EXPOSE 8001
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8001"]
