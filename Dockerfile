FROM ubuntu:jammy
# Set the working directory inside the container
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip



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
COPY ./llms /myapp/llms

COPY ./entrypoint.sh ./
# Expose the required ports
# EXPOSE 8000
# EXPOSE 8080
ENTRYPOINT ["sh","/myapp/entrypoint.sh"]