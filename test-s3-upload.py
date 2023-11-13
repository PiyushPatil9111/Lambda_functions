import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(local_file_path, bucket_name, s3_key):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file
        s3.upload_file(local_file_path, bucket_name, s3_key)
        print(f"File uploaded successfully to {bucket_name}/{s3_key}")
    except FileNotFoundError:
        print(f"The file {local_file_path} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")

# Replace these with your own values
local_file_path = r"D:\python_for_Lambda_func\Lambda_functions\file1.txt"
bucket_name = "killiana"
s3_key = "path/within/bucket/file1.txt"

upload_to_s3(local_file_path, bucket_name, s3_key)