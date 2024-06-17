#!/bin/bash

read -p "Enter name: " name
read -p "Enter age: " age

sudo docker-compose exec app /app/venv/bin/python -c "
import mysql.connector
conn = mysql.connector.connect(
    host='mysql',
    user='user',
    password='password',
    database='mydatabase'
)
cursor = conn.cursor()
cursor.execute('INSERT INTO users (Name, Age) VALUES (%s, %s)', ('$name', $age))
conn.commit()
cursor.close()
conn.close()
print('User inserted successfully!')
"
