# fastapi-s3-demo
Fast API that allows you to push text to a S3 bucket via post and a GET to retireve the contents

```
pip install fastapi uvicorn boto3
```



# Usage


```
curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@example.txt"
curl http://127.0.0.1:8000/download/example.txt
```

# swagger endpoint
```
http://127.0.0.1:8000/docs
```

# bucket information

Name: `arn:aws:s3:::42testbucket`  
Region: ` us-east-2`


Bucket Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:user/YOUR_IAM_USER_NAME"
      },
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::YOUR_BUCKET_NAME",
        "arn:aws:s3:::YOUR_BUCKET_NAME/*"
      ]
    }
  ]
}
```

IAM Policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::YOUR_BUCKET_NAME",
        "arn:aws:s3:::YOUR_BUCKET_NAME/*"
      ]
    }
  ]
}
```


