from flask import Flask, render_template, render_template, request, redirect, session
from . import auth, queries, uploads
from .utils import Settings

app = Flask(__name__)
app.secret_key = Settings().secret_key

API_BASE_URL = "http://app:8080"  # Replace with the actual base URL of your API

# Register blueprints
app.register_blueprint(auth.auth_bp)
app.register_blueprint(queries.query_bp)
app.register_blueprint(uploads.upload_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
