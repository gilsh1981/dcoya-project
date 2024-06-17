
Overview:
This project is a submission for the Dcoya Integration Challenge 2024. The goal of the challenge is to deploy a web application in clients' on-premise environments, ensuring the app is fully usable. The application consists of two main components: a MySQL database and a web application, both running in Docker containers.

Prerequisites: Setting Up Docker and Docker Compose
Before starting with the specific tasks, Docker and Docker Compose were installed and configured on an Ubuntu VM.

Install Docker and Docker Compose:

sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo apt install -y curl
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

Set up project directory:

mkdir ~/dcoya-project
cd ~/dcoya-project
Task 1: MySQL Docker Container
Created a Docker container based on the latest MySQL database:

Added the MySQL service to the docker-compose.yml file.
version: '3'
services:
  mysql:
    image: mysql:latest
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    volumes:
      - ./mysql:/docker-entrypoint-initdb.d
    ports:
      - "3306:3306"

      Wrote a script to create a users table:

mysql/init_db.sql:
CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase;
CREATE TABLE IF NOT EXISTS users (
  Name VARCHAR(255),
  Age INT
);

Configured the script to run on each boot by placing it in the ./mysql directory, which is mapped to /docker-entrypoint-initdb.d in the MySQL container.

Task 2: Application Docker Container
Created a Docker container based on a minimal build of the latest Ubuntu LTS distribution:

Added the app service to the docker-compose.yml file and created a Dockerfile.
services:
  app:
    build: ./app
    ports:
      - "5000:5000"
    depends_on:
      - mysql
app/Dockerfile:
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

Wrote a “data insert” script:

Implemented in app.py.
from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host="mysql",
        user="user",
        password="password",
        database="mydatabase"
    )
    return connection

@app.route('/')
def insert_user():
    return render_template('insert.html')

@app.route('/insert', methods=['POST'])
def insert():
    name = request.form['name']
    age = request.form['age']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (Name, Age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cursor.close()
    conn.close()
    return 'User inserted successfully! <a href="/read">View Users</a>'

@app.route('/read')
def read_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('users.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

      app/templates/insert.html:
<!-- insert.html -->
<form action="/insert" method="post">
    Name: <input type="text" name="name"><br>
    Age: <input type="text" name="age"><br>
    <input type="submit" value="Insert">
</form>

Wrote a “data read” script:

Included in app.py as the /read route.
app/templates/users.html:
<!-- users.html -->
<table border="1">
    <tr>
        <th>Name</th>
        <th>Age</th>
    </tr>
    {% for row in rows %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
    </tr>
    {% endfor %}
</table>
<br>
<a href="/">Insert New User</a>

Task 3: Docker Host Virtual Image
Installed Ubuntu VM and Docker Compose (as done in the prerequisites).

Deploy the containers:
cd ~/dcoya-project
sudo docker-compose up -d

Task 4: Using an External Machine
Set up SSH on the Ubuntu VM:
sudo apt-get install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh

Find the IP address of your Ubuntu VM:

ip addr show
ssh username@ip_address


cd ~/dcoya-project
./insert_user.sh
./read_users.sh

Task 5: Pack the Docker Host VM into an OVA Image
Shut down the VM:

sudo shutdown now


Export the VM to an OVA file:

Open VirtualBox.
Right-click on the VM and select "Export to OCI...".
Follow the prompts to export the VM as an OVA file.
Task 6: Additional Challenges
Secure Connection Using SSL
Generate SSL certificates for MySQL and the application:

# Generate MySQL SSL certificates
mkdir -p ~/mysql-ssl
cd ~/mysql-ssl
openssl genrsa 2048 > ca-key.pem
openssl req -new -x509 -nodes -days 3600 -key ca-key.pem -out ca.pem
openssl req -newkey rsa:2048 -days 3600 -nodes -keyout server-key.pem -out server-req.pem
openssl rsa -in server-key.pem -out server-key.pem
openssl x509 -req -in server-req.pem -days 3600 -CA ca.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem

Configure MySQL to use SSL:

Add the following lines to your my.cnf file (usually located at /etc/mysql/my.cnf):
[mysqld]
ssl-ca=/path/to/ca.pem
ssl-cert=/path/to/server-cert.pem
ssl-key=/path/to/server-key.pem

Modify the application to connect to MySQL using SSL:
def get_db_connection():
    connection = mysql.connector.connect(
        host="mysql",
        user="user",
        password="password",
        database="mydatabase",
        ssl_ca='/path/to/ca.pem',
        ssl_cert='/path/to/client-cert.pem',
        ssl_key='/path/to/client-key.pem'
    )
    return connection


Logging Requests
Modify the application to log all requests:
import logging

logging.basicConfig(filename='app/logs/app.log', level=logging.INFO)

@app.route('/insert', methods=['POST'])
def insert():
    name = request.form['name']
    age = request.form['age']
    if not name or





