FROM python:3.10-slim-buster
# Set the working directory inside the container
WORKDIR /myapp

# Copy the requirements.txt file to the container
COPY ./requirements.txt /myapp/requirements.txt

# Install the Python dependencies
RUN pip install -r /myapp/requirements.txt
#--no-cache-dir 
# Copy the FastAPI application code to the container
COPY ./app /myapp/app
COPY ./authapp /myapp/authapp
COPY ./frontend /myapp/frontend

COPY ./entrypoint.sh ./
# Expose the required ports
# EXPOSE 8000
# EXPOSE 8080
ENTRYPOINT ["sh","/myapp/entrypoint.sh"]