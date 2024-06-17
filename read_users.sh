#!/bin/bash

sudo docker-compose exec app /app/venv/bin/python -c "
import mysql.connector
conn = mysql.connector.connect(
    host='mysql',
    user='user',
    password='password',
    database='mydatabase'
)
cursor = conn.cursor()
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
for row in rows:
    print(f'Name: {row[0]}, Age: {row[1]}')
cursor.close()
conn.close()
"
