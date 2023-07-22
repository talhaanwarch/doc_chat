from flask import Blueprint, render_template, request, session
import requests
import structlog

logger = structlog.getLogger()
query_bp = Blueprint("query", __name__)
API_BASE_URL = "http://app:8080" 

@query_bp.route("/query", methods=["GET", "POST"])
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
                logger.info("query")
                logger.info(query_result)
                return render_template("query.html", user_email=user_email, user_input=user_input,
                                       output=query_result.get('answer', ''), error=query_result.get('error', ''))

            # Render the query.html template without user input initially
            return render_template("query.html", user_email=user_email)

    return redirect("/login")
