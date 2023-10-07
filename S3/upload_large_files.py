# Upload large files to S3

import boto3
from boto3.s3.transfer import TransferConfig


s3_client = boto3.client("s3")

S3_BUCKET = "S3_BUCKET"  # Change
FILE_PATH = "FILE_PATH_LOCATION_ON_SYSTEM"  # Change
KEY_PATH = "S3_FILE_PATH"  # CHANGE


def uploadFileS3(file_path):
    config = TransferConfig(
        multipart_threshold=512 * 1024 * 1024,  # 500 MB
        max_concurrency=10,
        multipart_chunksize=512 * 1024 * 1024,  # 500 MB
        use_threads=True,
    )
    s3_client.upload_file(file_path, S3_BUCKET, KEY_PATH, Config=config)


uploadFileS3(FILE_PATH)
