from flask import Blueprint, render_template, redirect, request, session
import requests

auth_bp = Blueprint("auth", __name__)
API_BASE_URL = "http://app:8080" 

@auth_bp.route("/register", methods=["GET", "POST"])
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


@auth_bp.route("/login", methods=["GET", "POST"])
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


@auth_bp.route("/logout")
def logout():
    # Clear the session and redirect to the logout page
    session.clear()
    return render_template("logout.html")
