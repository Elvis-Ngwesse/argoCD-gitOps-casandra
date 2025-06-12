from flask import Flask, jsonify
import boto3
import os
from urllib.parse import urlparse, urlunparse

app = Flask(__name__)

# Load MinIO connection info from environment
endpoint = os.environ['MINIO_ENDPOINT']  # e.g. http://minio-service:9000
access_key = os.environ['AWS_ACCESS_KEY_ID']
secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
bucket = os.environ['MINIO_BUCKET']

s3 = boto3.client(
    's3',
    endpoint_url=endpoint,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    config=boto3.session.Config(signature_version='s3v4')
)

LOCAL_HOST = 'localhost:9000'  # replace with your local forwarded endpoint


@app.route('/presigned-urls')
def presigned_urls():
    try:
        objects = s3.list_objects_v2(Bucket=bucket, Prefix='results/')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if 'Contents' not in objects:
        return jsonify({"files": []})

    files = objects['Contents']

    urls = {}
    for obj in files:
        key = obj['Key']
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=3600  # 1 hour expiry
        )
        # Replace hostname in URL with localhost:9000 for local access
        parsed = urlparse(url)
        # Construct new URL with localhost:9000 as netloc
        new_url = urlunparse(parsed._replace(netloc=LOCAL_HOST))
        urls[key] = new_url

    return jsonify(urls)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
