import os
import boto3
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.models import APIKey
from fastapi.openapi.models import APIKeyIn
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# Setup boto3 client
s3_client = boto3.client("s3")

S3_BUCKET = os.getenv("S3_BUCKET")  # Load the S3 bucket from environment variable


class PreSignedUrlResponse(BaseModel):
    presigned_url: str


@app.get("/presign/{s3_key}", response_model=PreSignedUrlResponse)
async def get_presigned_url(s3_key: str):
    try:
        # Generate a pre-signed URL for the object
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": s3_key},
            ExpiresIn=3600,  # The URL will be valid for 1 hour by default
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating pre-signed URL")

    if not presigned_url:
        raise HTTPException(
            status_code=404, detail="Failed to generate the presigned URL"
        )

    return {"presigned_url": presigned_url}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# serve OpenAPI yaml file
app.mount("/docs", StaticFiles(directory="docs", html=True), name="docs")
