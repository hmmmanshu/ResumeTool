import boto3
import config
from config import Config
s3_client = boto3.client('s3',aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
 region_name=config.Config.S3_REGION)

def upload_file_to_s3(file):
    file_key = f"resumes/{file.filename}"
    s3_client.upload_fileobj(file, Config.S3_BUCKET, file_key)
    return f"https://{Config.S3_BUCKET}.s3.amazonaws.com/{file_key}"
