/* This JS script is responsible for sending a request to the /users route.
This function gets called as soon as the login page finishes loading and
immediately sends a request to the /users route. In app.py, this route is
configured to call the select_user method from keypadLogin.py. Effectively,
this script makes it possible to start listening to the external keypad without
any additional input from the user. */
document.addEventListener("DOMContentLoaded", (event) =>{
	console.log('webpage loaded');
	fetch('/users')
		.then(response => response.json())
		.then(function(response) {
			console.log(response);
			// This gets the response (which is A, B, C, or D from the keypad)
			// and injects it on the webpage so users can confirm they selected
			// the correct user.
			user_id = response['user_id'];
			document.getElementById('header').innerHTML = 'Selected User: ' + user_id;
			// This tells the users that they should now enter their 4 digit pin
			document.getElementById('post-user').innerHTML = `Please enter 4
				digit pin on keypad. Press \"#\" to reset the erase entered
				digits and start over. To select another user, press \"*\".`
			
			// This part of the script acts as an intersection between the
			// different web pages. It starts off by sending a request to
			// /user/{user_id}.
			user_url = '/user/' + user_id;
			fetch(user_url)
				.then(response => response.json())
				.then(function(response) {
					console.log(response);
					// If a user presses '*' on the keypad, this reloads the
					// current page so that the user can choose another user
					// from the keypad.
					if (response['page'] == -1) document.location.reload();
					// This redirects the user to the incorrect login page,
					// which itself redirects to the main login page
					// after 2 seconds. The '_self' tag makes it so that the
					// incorrect login page is opened in the same tab.
					else if (response['page'] == 0) window.open('http://localhost:6543/incorrect', '_self');
					// This means that an authorized user has entered a correct
					// password. This redirects them to the main sensors
					// dashboard where they can make their sensor queries.
					else if (response ['page'] == 1) window.open('http://localhost:6543/sensors/-1/-1', '_self');
				});
		});
})