from flask import Blueprint, render_template, request, session, redirect
import requests
import boto3
from .utils import Settings
import structlog

upload_bp = Blueprint("upload", __name__)
logger = structlog.getLogger()
API_BASE_URL = "http://app:8080" 

@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():
    access_token = session.get("access_token")
    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_BASE_URL}/authenticated-route", headers=headers)
        if response.status_code == 200:
            user_email = response.json().get("message").split()[1]

            if request.method == "POST":
                # Add upload logic here
                files = request.files.getlist('files')

                s3 = boto3.client(service_name='s3',
                                  region_name=Settings().region_name,
                                  aws_access_key_id=Settings().aws_access_key_id,
                                  aws_secret_access_key=Settings().aws_secret_access_key)
                s3_uris = []
                for file in files:
                    if file.filename.endswith('.pdf'):
                        s3.upload_fileobj(file, Settings().bucket_name, file.filename)
                        s3_uri = f's3://{Settings().bucket_name}/{file.filename}'
                        s3_uris.append(s3_uri)
                logger.info("s3_uri")
                logger.info(s3_uris)

                query_data = {"urls": s3_uris}
                query_response = requests.post(f"{API_BASE_URL}/ingest", headers=headers, json=query_data)

                if query_response.status_code == 200:
                    query_result = query_response.json()
                else:
                    # Handle the query error appropriately
                    query_result = {"error": "An error occurred during the query."}

                return render_template("upload.html", user_email=user_email, output=query_result)

            # Render the upload.html template without user input initially
            return render_template("upload.html", user_email=user_email)

    return redirect("/login")
