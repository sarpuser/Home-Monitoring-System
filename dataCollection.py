import RPi.GPIO as GPIO
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import time
from Library import UltrasonicRanging as US
from Library import SenseLED as IR

# Load environment variables and assign them to local variables
load_dotenv("./Setup/credentials.env")
 
''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Connect to the database
db = mysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
cursor = db.cursor()

# Pinout - the Ultrasound pin is defined in UltrasonicRanging.py
irPin = 21

if __name__ == '__main__':     # Program entrance
	print ('Program is starting...')
	# Set up the sensors
	US.setup()
	IR.setup()
	try:
		# This will keep collecting data until the program is stopped
		while(True):
			distance = US.getSonar() # get distance
			print ("The distance is : %.2f cm"%(distance))
			# Get the value of the irPin (1 for motion detected, 0 otherwise)
			motion = GPIO.input(irPin)
			print ('IR output: %d' %motion)
			# Add the sensor data to the database
			cursor.execute('INSERT INTO Sensor_Data (us_distance, ir_motion) VALUE (%s, %s)' %(distance, motion))
			# We need db.commit so that the changes are saved to the database
			db.commit()
			# Sleep for one second. This adjusts the pulling rate of the
			# sensors. A higher sleep time means less frequent data recording.
			time.sleep(1)
	except KeyboardInterrupt:  # Press ctrl-c to end the program.
		GPIO.cleanup()         # release GPIO resource