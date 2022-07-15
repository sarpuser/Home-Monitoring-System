from unittest import result
import mysql.connector as mysql

import os
import datetime
from dotenv import load_dotenv #only required if using dotenv for credentials

# Load environment variables
load_dotenv("credentials.env")

# Set values of local variables to the db credentials from env variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
 
# Connect to MySQl
db = mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()
 
# Create ECE140A_Midterm database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS ECE140A_Midterm")

# Connect to the ECE140A_Midterm DB
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# Delete the old User_Pins table if it exists
cursor.execute("DROP TABLE IF EXISTS User_Pins;")
 
# Try to create table. Print error if it doesn't work.
try:
	cursor.execute("""
		CREATE TABLE User_Pins (
			id          CHAR(1) PRIMARY KEY,
			name        VARCHAR(50) NOT NULL,
			pin			CHAR(4) NOT NULL,
			authorized	INT NOT NULL
		);
	""")
except RuntimeError as err:
	print("runtime error: {0}".format(err))

# Populate table with user data
query = "INSERT INTO User_Pins (id, name, pin, authorized) VALUES (%s, %s, %s, %s)"
values = [
	('A','Sarp','6789', 1),
	('B','Kyle','1234', 1),
	('C','Ramsin','4321', 0),
	('D','Rick','9876', 0)
]
cursor.executemany(query, values)
db.commit()

# Print created table for confirmation
cursor.execute('SELECT * FROM User_Pins')
result = cursor.fetchall()
print ('Created User_Pins Table:')
print ('------------------------')
[print(x) for x in result]

# Try to create table if it doesn't already exist. Print error if it doesn't work.
try:
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS Sensor_Data(
			id          INT AUTO_INCREMENT PRIMARY KEY,
			ir_motion	INT,
			us_distance	FLOAT,
			time		TIMESTAMP
		);
	""")
except RuntimeError as err:
	print("runtime error: {0}".format(err))