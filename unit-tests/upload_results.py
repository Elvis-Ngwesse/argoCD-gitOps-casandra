import boto3
import os
from botocore.exceptions import ClientError

bucket = os.environ['MINIO_BUCKET']
endpoint = os.environ['MINIO_ENDPOINT']
access_key = os.environ['AWS_ACCESS_KEY_ID']
secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
timestamp = os.environ['TIMESTAMP']  # ✅ Now consistent

s3 = boto3.client(
    's3',
    endpoint_url=endpoint,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

try:
    s3.head_bucket(Bucket=bucket)
except ClientError:
    s3.create_bucket(Bucket=bucket)

s3.upload_file(f'results_{timestamp}.xml', bucket, f'results/results_{timestamp}.xml')
s3.upload_file(f'results_{timestamp}.html', bucket, f'results/results_{timestamp}.html')

print('✅ Uploaded test artifacts to MinIO')
