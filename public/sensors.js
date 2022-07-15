// This function sends a request to /911 and then immediately opens the user
// selection page.
function emergency() {
	fetch('/911')
		.then(window.open('http://localhost:6543', '_self'))
}

/* This function is responsible for getting the values from the dropdown menus
and then opening the correct url. The reason we are just opening the url
instead of converting the response to JSON and then doing stuff to that
response is because we are using jinja t render the file. We therefore do not
need JS to inject content into the screen. */
function get_data() {
	sensor_id = document.getElementById('sensor').value
	time_frame = document.getElementById('time-frame').value

	url = '/sensors/' + sensor_id + '/' + time_frame
	window.open(url, '_self')
}

// This function opens the user selection page
function logout() {
	window.open('http://localhost:6543', '_self')
}