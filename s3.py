import boto3
import os
import pandas as pd

def read_files_from_s3(bucket_name, file_keys):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    data_frames = {}
    for file_key in file_keys:
        obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        if file_key.endswith('.csv'):
            data_frames[file_key] = pd.read_csv(obj['Body'])
        else:
            st.error(f"Unsupported file format for {file_key}")
    
    return data_frames