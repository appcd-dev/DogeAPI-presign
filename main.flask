import os

from flask import Flask, jsonify, abort, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import boto3


app = Flask(__name__)

# Setup OpenAPI
SWAGGER_URL = '/docs'
API_URL = '/docs/openapi.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Presign API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Setup boto3 client
s3_client = boto3.client("s3")

S3_BUCKET = os.getenv("S3_BUCKET")  # Load the S3 bucket from environment variable


@app.route("/presign/<s3_key>", methods=["GET"])
def get_presigned_url(s3_key):
    try:
        # Generate a pre-signed URL for the object
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": s3_key},
            ExpiresIn=3600,  # The URL will be valid for 1 hour by default
        )
    except Exception as e:
        abort(500, description="Error generating pre-signed URL")

    if not presigned_url:
        abort(404, description="Failed to generate the presigned URL")

    return jsonify({"presigned_url": presigned_url})


@app.route('/docs/openapi.yaml')
def serve_openapi():
    return send_from_directory('docs', 'openapi.yaml')


if __name__ == "__main__":
    app.run(debug=True)
