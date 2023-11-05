# utils/s3_util.py
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os
from fastapi import UploadFile

from fastapi import HTTPException

load_dotenv()

s3_client = boto3.client('s3',
                         aws_access_key_id=os.getenv("AWS_ACCESS_KEY"), 
                         aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
                         )#, region_name='us-east-2

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

async def upload_file_to_s3(file: UploadFile):
    try:
        file_content = await file.read()
        s3_client.put_object(Bucket=BUCKET_NAME, Key=file.filename, Body=file_content)
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file.filename}"
        return file_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Could not connect to AWS with provided credentials")
    except Exception as e:
        raise   HTTPException(status_code=500, detail=f"An error ocurred: {str(e)}")

