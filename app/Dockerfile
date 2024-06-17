FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv mysql-client

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create and activate a virtual environment, install dependencies
RUN python3 -m venv venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install mysql-connector-python flask

# Copy entry point script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Ensure the entry point uses the virtual environment's Python
ENTRYPOINT ["/app/venv/bin/python"]
CMD ["app.py"]

