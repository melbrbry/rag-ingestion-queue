import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile
from loguru import logger


def get_s3_client():
    """Create and return an S3 client."""
    return boto3.client("s3")


def save_file(file: UploadFile, job_id: str, bucket_name: str) -> str:
    """
    Upload the file to S3.
    Returns the S3 key (object name).
    """
    s3_client = get_s3_client()
    object_key = f"{job_id}_{file.filename}"

    try:
        s3_client.upload_fileobj(file.file, bucket_name, object_key)
        logger.info(f"Successfully uploaded '{file.filename}' to 's3://{bucket_name}/{object_key}'")
        return object_key
    except ClientError as e:
        logger.error(f"Failed to upload file to S3: {e}")
        raise


def download_file(object_key: str, bucket_name: str, local_path: str) -> str:
    """
    Download a file from S3 to local path.
    Returns the local file path.
    """
    s3_client = get_s3_client()

    try:
        s3_client.download_file(bucket_name, object_key, local_path)
        logger.info(f"Successfully downloaded 's3://{bucket_name}/{object_key}' to '{local_path}'")
        return local_path
    except ClientError as e:
        logger.error(f"Failed to download file from S3: {e}")
        raise
