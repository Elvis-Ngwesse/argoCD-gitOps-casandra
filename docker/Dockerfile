FROM python:3.10-slim
WORKDIR /app
COPY app/ /app
RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 8001
CMD ["python", "main.py"]
