from flask import Flask, render_template, request, redirect, session
import requests
import boto3
from .utils import Settings
import structlog
logger = structlog.getLogger()

app = Flask(__name__)
app.secret_key = Settings().secret_key # Set a secret key for session management

API_BASE_URL = "http://app:8080"  # Replace with the actual base URL of your API


@app.route("/")
def index():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Process registration form data and make a POST request to the registration endpoint
        data = {
            "email": request.form.get("email"),
            "password": request.form.get("password"),
        }
        response = requests.post(f"{API_BASE_URL}/auth/register", json=data)
        if response.status_code == 201:
            # Registration successful, redirect to login page
            return redirect("/login")
        else:
            # Registration failed, handle the error appropriately
            error_message = response.json().get("detail")
            return render_template("register.html", error_message=error_message)

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Process login form data and make a POST request to the login endpoint
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'username': request.form.get("email"),
            'password': request.form.get("password"),
        }

        response = requests.post(f"{API_BASE_URL}/auth/jwt/login", headers=headers, data=data)

        if response.status_code == 200:
            # Login successful, store the JWT token in the session
            session["access_token"] = response.json().get("access_token")
            return redirect("/query")
        else:
            # Login failed, handle the error appropriately
            error_message = response.json().get("detail")
            return render_template("login.html", error_message=error_message)

    return render_template("login.html")


@app.route("/logout")
def logout():
    # Clear the session and redirect to the logout page
    session.clear()
    return render_template("logout.html")


@app.route("/query", methods=["GET", "POST"])
def query():
    access_token = session.get("access_token")
    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_BASE_URL}/authenticated-route", headers=headers)
        if response.status_code == 200:
            user_email = response.json().get("message").split()[1]

            if request.method == "POST":
                # Retrieve the user input from the form
                user_input = request.form.get("input")

                # Send a POST request to the /query endpoint with user_input
                query_data = {"text": user_input}
                query_response = requests.post(f"{API_BASE_URL}/query", headers=headers, json=query_data)

                if query_response.status_code == 200:
                    query_result = query_response.json()
                else:
                    # Handle the query error appropriately
                    query_result = {"error": "An error occurred during the query."}

                return render_template("query.html", user_email=user_email, user_input=user_input,
                                       output=query_result.get('answer', ''), error=query_result.get('error', ''))

            # Render the query.html template without user input initially
            return render_template("query.html", user_email=user_email)

    return redirect("/login")


@app.route("/upload", methods=["GET", "POST"])
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
                logger.info( s3_uris)

                query_data = {"urls": s3_uris}
           
                headers = {"Authorization": f"Bearer {access_token}"}
                query_response = requests.post(f"{API_BASE_URL}/ingest", headers=headers, json=query_data)

                if query_response.status_code == 200:
                    query_result = query_response.json()
                else:
                    # Handle the query error appropriately
                    query_result = {"error": "An error occurred during the query."}


                return render_template("upload.html", user_email=user_email, output = query_result)

            # Render the upload.html template without user input initially
            return render_template("upload.html", user_email=user_email)

    return redirect("/login")
