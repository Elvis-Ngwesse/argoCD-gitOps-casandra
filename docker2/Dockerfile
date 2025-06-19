FROM python:3.10-slim

WORKDIR /app

COPY app2/ /app
RUN pip install -r requirements.txt
ENV MINIO_ENDPOINT=http://minio-service:9000
ENV MINIO_BUCKET=test-reports
ENV AWS_ACCESS_KEY_ID=minioadmin
ENV AWS_SECRET_ACCESS_KEY=minioadmin

EXPOSE 5002

CMD ["python", "main.py"]
