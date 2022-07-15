# This script is used to delete all recorded sensor values. Use with caution!

from unittest import result
import mysql.connector as mysql

import os
from dotenv import load_dotenv #only required if using dotenv for credentials

# Load environment variables
load_dotenv("credentials.env")

# Set values of local variables to the db credentials from env variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
 
# Connect to MySQl
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# Drop the Sensor_Data table (reset all sensor recordings)
cursor.execute('DROP TABLE Sensor_Data')
db.commit()
db.close()