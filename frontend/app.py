from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session management

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
            return redirect("/protected")
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


@app.route("/protected", methods=["GET", "POST"])
def protected():
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
                    # print('Query Response:', query_result)
                
                return render_template("protected.html", user_email=user_email, user_input=user_input, output = query_result['answer'] )
            
            # Render the protected.html template without user input initially
            return render_template("protected.html", user_email=user_email)
    
    return redirect("/login")




# if __name__ == "__main__":
#     app.run()
