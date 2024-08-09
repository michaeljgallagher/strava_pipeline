import boto3
from botocore.exceptions import NoCredentialsError


def connect_s3():
    """
    Create a boto3 session and connect to the S3 Resource

    Returns:
        connection to the S3 bucket
    """
    try:
        s3 = boto3.resource("s3")
        return s3
    except NoCredentialsError as e:
        raise e


def upload_to_s3(src: str, bucket: str, dst: str):
    """
    Upload file to S3 bucket

    Args:
        src (str): source file
        bucket (str): bucket name
        dst (str): destination name
    """
    s3 = connect_s3()
    s3.meta.client.upload_file(Filename=src, Bucket=bucket, Key=dst)
