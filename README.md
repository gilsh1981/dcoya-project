Dcoya Integration Challenge 2024 Completed! 


## Prerequisites

- **Docker Compose**: Used for creating and managing Docker containers.
    - **MySQL Container**: For the MySQL database.
    - **App Container**: For the web application.

- **MySQL Database**: 
    - Configured with user, password, and initial database setup.
    - Used to store user data with a `users` table.

- **Web Application**: 
    - Developed using Python and Flask.
    - Connects to MySQL to insert and retrieve user data.

- **Ubuntu VM**: 
    - Host for Docker and Docker Compose.
    - Configured with OpenSSH for remote access.

- **SSL Certificates**: 
    - Generated for secure communication with MySQL.
    - Configured to use in the web application for secure database connections.

- **Logging**: 
    - Implemented to log all requests for auditing and debugging purposes.

## Setup Steps Overview

1. **Docker and Docker Compose Installation**:
    - Install Docker and Docker Compose on Ubuntu VM.
    - Ensure Docker service is running and enabled at startup.

2. **Project Directory Setup**:
    - Create a directory for the project.
    - Add Docker Compose file and necessary scripts.

3. **MySQL and App Container Setup**:
    - Define services in Docker Compose.
    - Create initialization scripts for the MySQL database.
    - Develop Flask web application to interact with the database.

4. **SSH Configuration**:
    - Enable and start SSH service on the Ubuntu VM.
    - Use SSH for remote management and deployment.

5. **OVA Image Export**:
    - Export the configured VM as an OVA file for easy deployment.

6. **Additional Security and Features**:
    - Implement SSL for secure MySQL connections.
    - Add logging for application requests.


