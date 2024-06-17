Dcoya Integration Challenge 2024
Overview
This project is a submission for the Dcoya Integration Challenge 2024. The goal is to deploy a web application in clients' on-premise environments. The application consists of two main components: a MySQL database and a web application, both running in Docker containers.

Prerequisites
Ensure Docker and Docker Compose are installed and configured on an Ubuntu VM.

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
Create a Docker container based on the latest MySQL database.

docker-compose.yml:
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


Initialization Script:
-- mysql/init_db.sql
CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase;
CREATE TABLE IF NOT EXISTS users (
  Name VARCHAR(255),
  Age INT
);


Task 2: Application Docker Container
Create a Docker container based on a minimal build of the latest Ubuntu LTS distribution.

docker-compose.yml:
services:
  app:
    build: ./app
    ports:
      - "5000:5000"
    depends_on:
      - mysql


Dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv mysql-client
WORKDIR /app
COPY . /app
RUN python3 -m venv venv && /app/venv/bin/pip install --upgrade pip && /app/venv/bin/pip install mysql-connector-python flask
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/venv/bin/python"]
CMD ["app.py"]


app.py:
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


Task 3: Deploy Containers
cd ~/dcoya-project
sudo docker-compose up -d


Task 4: SSH Setup
Set up SSH on the Ubuntu VM:

sudo apt-get install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh


Task 5: Export VM to OVA
Shut down the VM and export it to an OVA file via VirtualBox.

Task 6: Additional Challenges
Secure MySQL with SSL and implement request logging.

SSL Certificates:
mkdir -p ~/mysql-ssl
cd ~/mysql-ssl
openssl genrsa 2048 > ca-key.pem
openssl req -new -x509 -nodes -days 3600 -key ca-key.pem -out ca.pem
openssl req -newkey rsa:2048 -days 3600 -nodes -keyout server-key.pem -out server-req.pem
openssl rsa -in server-key.pem -out server-key.pem
openssl x509 -req -in server-req.pem -days 3600 -CA ca.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem


Logging:
import logging
logging.basicConfig(filename='app/logs/app.log', level=logging.INFO)


Repository Structure:
dcoya-project/
docker-compose.yml
mysql/
init_db.sql
app/
Dockerfile
app.py
entrypoint.sh
templates/
insert.html
users.html


How to Run
Clone the repository.
Navigate to the project directory.
Deploy the containers using Docker Compose.
sudo docker-compose up -d
Access the web application at http://localhost:5000.


