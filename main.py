import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

# Load environment variables from a .env file (optional)
load_dotenv()

app = FastAPI()

# S3 client configuration using environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
bucket_name = os.getenv('AWS_BUCKET_NAME')

if not all([aws_access_key_id, aws_secret_access_key, aws_region, bucket_name]):
    raise RuntimeError("Missing required environment variables")

s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

class S3Object(BaseModel):
    key: str
    content: str

@app.post("/upload/")
async def upload_object(file: UploadFile = File(...)):
    try:
        s3_client.upload_fileobj(file.file, bucket_name, file.filename)
        return {"message": "File uploaded successfully"}
    except (NoCredentialsError, PartialCredentialsError):
        raise HTTPException(status_code=403, detail="Invalid AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/upload/")
async def put_object(obj: S3Object):
    try:
        s3_client.put_object(Bucket=bucket_name, Key=obj.key, Body=obj.content)
        return {"message": "Object written successfully"}
    except (NoCredentialsError, PartialCredentialsError):
        raise HTTPException(status_code=403, detail="Invalid AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{key}")
async def get_object(key: str):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read().decode('utf-8')
        return {"key": key, "content": content}
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Object not found")
    except (NoCredentialsError, PartialCredentialsError):
        raise HTTPException(status_code=403, detail="Invalid AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
