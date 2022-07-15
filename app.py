from re import U
from urllib import response
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
from pyramid.renderers import render_to_response
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import time
import math
from Library import keypadLogin as login
from Library import buzzer

# Load environment variables and assign them to local variables
load_dotenv("./Setup/credentials.env")
 
''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

''' Home Page '''
def get_home(req):
	return FileResponse("./HTML/login.html")

''' Select User'''
def select_user(req):
	# This get a correct user ID (A, B, C, or D) from the keypad
	user_id = login.selectUser()
	return {'user_id': user_id}

''' Login with pin'''
def pinLogin(req):
	user_name = req.matchdict['user_id'] # Find the user ID from the request
	# This is what handles the pin entry by the user. user_pin will either be
	# -1 if a user presses '*' or it will be the 4 digit pin the user has entered.
	user_pin = login.getUserPin()

	# If user_pin is -1 (user pressed '*'), return {'page': -1}. login.js will
	# see this response and reload login.html so that the user may choose
	# another user.
	if (user_pin == '-1'):
		print('Going back to login')
		return {'page': -1}

	# Connect to the database
	db = mysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	cursor = db.cursor()

	# This MySQL line gets the value of 'authorized' from the User_Pins table.
	# If the pin the user entered does not match that on the database, the
	# query won't return anything since there won't be any lines that match the
	# ID and user entered pin.
	cursor.execute('SELECT authorized FROM User_Pins WHERE id=\'%s\' AND pin=\'%s\';' %(user_name, user_pin))
	user = cursor.fetchone()
	# If there is nothing returned from the query, user entered an incorrect pin
	if (user == None):
		print ('Unauthorized')
		return {'page': 0}
	else:
		# If the query returned a value, we now need to check if user has access
		# We use user[0] since value returned from query is a tuple
		user_authorized = user[0]
		# If user is authorized we return 1 telling login.js tp redirect
		# to the sensor data
		if (user_authorized):
			print ('Correct login')
			return {'page': 1}
		# If user is unauthorized, we return 0, telling login.js to redirect to
		# incorrect login/ unauthorized user page
		else:
			print('Unauthorized')
			return {'page': 0}

''' Incorrect Login/ Unauthorized User '''
def incorrect(req):
	return FileResponse("./HTML/incorrect.html")

''' Display Sensor Data '''
def sensors(req):
	sensor_id = int(req.matchdict['sensor_id'])
	time_frame = int(req.matchdict['time_frame'])

	# Connect to the database
	db = mysql.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
	cursor = db.cursor()

	# This is when no parameters are selected. It returns the last 100 entries
	if (sensor_id == -1 and time_frame == -1):
		cursor.execute('''SELECT us_distance, ir_motion, time FROM Sensor_Data
						ORDER BY id DESC LIMIT 100;''')
		records = cursor.fetchall()
		# The headers list in the JSON is what jinja2 will use to print out the
		# column headers
		response = {'records': records, 'headers': ['Distance', 'Motion', 'Time']}
	# This is if a time frame has been selected but no sensor selected
	elif (sensor_id == -1 and time_frame != -1):
		# time.time() returns epoch seconds (seconds since Jan 1st 19170).
		# We use floor to round it down to an integer. We then subtract our
		# time frame (multiplied by 60 since the original value is in mins).
		# We do this since we are looking for the last x minutes of data.
		# So we get all the data that has a unix timestamp (converting the time
		# to epoch seconds) above our specified time frame.
		time_upper_bound = math.floor(time.time()) - (time_frame * 60)
		cursor.execute('''SELECT us_distance, ir_motion, time FROM Sensor_Data
						WHERE UNIX_TIMESTAMP(time) > %s ORDER BY id DESC;'''
						%time_upper_bound)
		records = cursor.fetchall()
		response = {'records': records, 'headers': ['Distance', 'Motion', 'Time']}
	# This is if a sensor is selected and a time frame is not
	elif (sensor_id != -1 and time_frame == -1):
		# sensor_id is 1 when ultrasound is selected
		if (sensor_id == 1):
			cursor.execute('''SELECT us_distance, time FROM Sensor_Data ORDER
							BY id DESC;''')
			records = cursor.fetchall()
			response = {'records': records, 'headers': ['Distance', 'Time']}
		# Otherwise, ir sensor is selected.
		else:
			cursor.execute('SELECT ir_motion, time FROM Sensor_Data ORDER BY id DESC;')
			records = cursor.fetchall()
			response = {'records': records, 'headers': ['Motion', 'Time']}
	# This is if both a sensor and a time frame has been selected
	elif (sensor_id != -1 and time_frame != -1):
		# We calculate the time frame in the same method as above
		time_upper_bound = math.floor(time.time()) - (time_frame * 60)
		if (sensor_id == 1):
			cursor.execute('''SELECT us_distance, time FROM Sensor_Data WHERE
							UNIX_TIMESTAMP(time) > %s ORDER BY id DESC;'''
							%time_upper_bound)
			records = cursor.fetchall()
			response = {'records': records, 'headers': ['Distance', 'Time']}
		else:
			cursor.execute('''SELECT ir_motion, time FROM Sensor_Data WHERE
							UNIX_TIMESTAMP(time) > %s ORDER BY id DESC;''' %time_upper_bound)
			records = cursor.fetchall()
			response = {'records': records, 'headers': ['Motion', 'Time']}

	db.close()
	return render_to_response("./HTML/sensors.html", response, request=req)

''' Emergency Alert '''
def emergency(req):
	# Sound the emergency alarm and return an empty JSON so that the JS file
	# does not throw an exception. The JS file also opens the login page.
	buzzer.emergencyAlarm()
	return {}

if __name__ == '__main__':
	with Configurator() as config:

		# to use Jinja2 to render the template! 
		config.include('pyramid_jinja2')
		config.add_jinja2_renderer('.html')
		
		# Configure route for user selection
		config.add_route('select_user', '/users')
		config.add_view(select_user, route_name='select_user', renderer='json')

		# Configure route for login with pin
		config.add_route('pinLogin', '/user/{user_id}')
		config.add_view(pinLogin, route_name='pinLogin', renderer='json')

		# Configure route for incorrect login/ unauthorized user
		config.add_route('incorrect', '/incorrect')
		config.add_view(incorrect, route_name='incorrect')

		# Configure route for displaying sensor data
		config.add_route('sensors', '/sensors/{sensor_id}/{time_frame}')
		config.add_view(sensors, route_name='sensors', renderer='json')

		# Configure route for emergency log off
		config.add_route('emergency', '/911')
		config.add_view(emergency, route_name='emergency', renderer='json')

		# Configure the route for the home page
		config.add_route('home', '/')
		config.add_view(get_home, route_name='home', renderer='json')

		# Configure the public resources
		config.add_static_view(name='/', path='./public', cache_max_age=3600)

		# Create server app
		app = config.make_wsgi_app()

# Start server 
server = make_server('0.0.0.0', 6543, app)
print('Web server started on: http://0.0.0.0:6543')
server.serve_forever()