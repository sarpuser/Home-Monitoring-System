document.addEventListener('DOMContentLoaded', (event) => {
	console.log('waiting 2 seconds');
	// This will wait for 2 seconds before redirecting to the home (login) page
	setTimeout(function(){
		window.open('http://localhost:6543', '_self');
	}, 2000);
})