from flask import Flask, jsonify
import boto3
import os
from urllib.parse import urlparse, urlunparse
import logging
import sys
from prometheus_flask_exporter import PrometheusMetrics  # ✅ Metrics

# ---------------------------------------
# ✅ Logging Setup
# ---------------------------------------
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("minio-url-service")

# ---------------------------------------
# 🌐 Flask App Setup
# ---------------------------------------
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

# ✅ Prometheus Metrics
metrics = PrometheusMetrics(app)

# ---------------------------------------
# 🔐 Load MinIO Environment Variables
# ---------------------------------------
try:
    endpoint = os.environ['MINIO_ENDPOINT']  # e.g. http://minio-service:9000
    access_key = os.environ['AWS_ACCESS_KEY_ID']
    secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
    bucket = os.environ['MINIO_BUCKET']
    logger.info("✅ Loaded environment variables for MinIO access")
except KeyError as e:
    logger.error("❌ Missing environment variable: %s", e)
    raise

# ---------------------------------------
# 🪣 Connect to MinIO (S3-Compatible)
# ---------------------------------------
s3 = boto3.client(
    's3',
    endpoint_url=endpoint,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    config=boto3.session.Config(signature_version='s3v4')
)

# For local development, replace MinIO hostname with this
LOCAL_HOST = 'localhost:9000'


# ---------------------------------------
# 🔗 Health & Root Route (Fixes 404)
# ---------------------------------------
@app.route('/')
def index():
    return jsonify({"status": "ok", "message": "MinIO Presigned URL Service is running"}), 200


# ---------------------------------------
# 🔗 Presigned URL Generator
# ---------------------------------------
@app.route('/presigned-urls')
def presigned_urls():
    logger.info("📥 Received request to generate presigned URLs")
    try:
        objects = s3.list_objects_v2(Bucket=bucket, Prefix='results/')
    except Exception as e:
        logger.error("❌ Failed to list objects in bucket %s: %s", bucket, e)
        return jsonify({"error": str(e)}), 500

    if 'Contents' not in objects:
        logger.info("📦 No objects found in bucket %s with prefix 'results/'", bucket)
        return jsonify({"files": []})

    urls = {}
    for obj in objects['Contents']:
        key = obj['Key']
        try:
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=3600  # 1 hour
            )
            parsed = urlparse(url)
            local_url = urlunparse(parsed._replace(netloc=LOCAL_HOST))
            urls[key] = local_url
            logger.info("🔗 Generated URL for key: %s", key)
        except Exception as e:
            logger.warning("⚠️ Failed to generate URL for key %s: %s", key, e)

    return jsonify(urls)


# ---------------------------------------
# 🚀 Run the App
# ---------------------------------------
if __name__ == '__main__':
    logger.info("🚀 MinIO Presigned URL Service starting on http://0.0.0.0:5002")
    app.run(host='0.0.0.0', port=5002)
