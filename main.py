from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = FastAPI()

# S3 client configuration
s3_client = boto3.client('s3', aws_access_key_id='YOUR_AWS_ACCESS_KEY', aws_secret_access_key='YOUR_AWS_SECRET_KEY', region_name='YOUR_AWS_REGION')
bucket_name = 'YOUR_BUCKET_NAME'

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
