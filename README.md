# fastapi-s3-demo
Fast API that allows you to push text to a S3 bucket via post and a GET to retireve the contents



Install dependencies
```
pip install fastapi uvicorn boto3 python-dotenv
```
or
```
pip install -r requirements.txt
```

To run this code for development, execute:
```
uvicorn main:app --reload
```

to run this code in a container
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

ensure that you set either a `.env` or a environmetn variable with the following values:
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_BUCKET_NAME
```


# Usage

Use a POST request via curl
```
curl -X POST "http://127.0.0.1:8000/upload/" -F "file=@example.txt"
```

Use a PUT request via curl
```
curl -X PUT "http://127.0.0.1:8000/upload/" -H "Content-Type: application/json" -d '{"key": "example.txt", "content": "This is a test content"}'
```

Get the content
```
curl http://127.0.0.1:8000/download/example.txt
```


Full example:
```
$ curl -X PUT "http://127.0.0.1:8000/upload/" -H "Content-Type: application/json" -d '{"key": "example.txt", "content": "This is a test content"}'           

{"message":"Object written successfully"}%                                                                                                                               ➜  

$ curl http://127.0.0.1:8000/download/example.txt
{"key":"example.txt","content":"This is a test content"}

```


# swagger endpoint
```
http://127.0.0.1:8000/docs
```

# bucket information

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


