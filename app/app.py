from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
import os
import logging

app = Flask(__name__)

# Configure logging
if not os.path.exists('/app/logs'):
    os.makedirs('/app/logs')
logging.basicConfig(filename='/app/logs/app.log', level=logging.INFO, format='%(asctime)s %(message)s')

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert():
    name = request.form['name']
    age = request.form['age']

    if not name.isalpha():
        logging.error("Invalid name entered")
        return "Invalid name. Please enter alphabetic characters only.", 400

    if not age.isdigit() or int(age) <= 0:
        logging.error("Invalid age entered")
        return "Invalid age. Please enter a positive integer.", 400

    age = int(age)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    conn.close()

    logging.info(f"Inserted user: {name}, age: {age}")
    return redirect(url_for('index'))

@app.route('/read')
def read():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('read.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
