# Project Description

In this midterm we were tasked to complete a joint hardware and software project where the material from the past five labs would be represented and utilized to their full extent with the addition of a raspberry pie and associated sensors. The implementation we designed used specifically utilized the infrared motion sensor, ultrasonic ranging sensor, keypad, and buzzer. The specific makeup of this design can be seen in the circuit diagram below. The basic concept that we wished to illustrate with this project was a security system that once the server was running and the instructions in the setup file were followed that could differentiate users with different access levels to view sensor data. Once on the website the keypad letters are used to cycle between four predefined users found in the init-db.py file two users have access to sensors and two do not and each has a password pin from which to enter the page with their associated access level. Other quality of life measures implemented into the login system were a redirect to login page upon incorrect password, star key returning the user to login screen, and pound key clearing user input. Once accessing the page with the proper authorization level to view the sensors the user can see the live recorded data being output to the page with two dropdown menus to denote which sensors data is being viewed and under what timeframe to view the recorded data. Lastly a user can hit the Emergency button on the page prompting the alarm to sound from the buzzer and a timed logoff from the webpage. [This is the associated video showing all of this functionality which was implemented for this project](https://drive.google.com/file/d/1AaRZFbtGPimownaySM25H6rTio56jcyj/view?usp=sharing) Major files in this project consist of a few varieties those within the Setup folder such as app.py and dataCollection.py which serves as the major components orchestrating the user requests and file responses for the HTML files and databases used in this project. The library folder consists of the python files that compose the logic behind the individual sensors, input, and output devices used in conjunction with the raspberry pie. A more comprehensive view of the respective folders and files used in this project can be found in the README inside of the Midterm folder. All in all, this project successfully illustrates the core concepts of the past five labs and has a focused functionality which exceeds basic functionality requirements outlined for this assignment. <br>
<br>
Here is the wiring diagram of the system: <br>
![wiring diagram](./Setup/Wiring%20Diagram.png)


# Code Organization

## The main code
The main code necessary for the midterm (`app.py` and `dataCollection.py`) are placed directly in the Midterm directory. These are the files that need to be run for the midterm.

## HTML
This folder includes all the HTML files that our website uses.

## Setup
This folder has code that only has to be run once, such as the database initialization code and the script to delete all recorded sensor data for a fresh start. Running `sensorDataReset.py` will permanently erase all recorded sensor data and **IT CANNOT BE UNDONE!!**

## Library
This folder includes all the background code for the various routes in `app.py` as well as the setup code for the sensors for `dataCollection.py`. These files do not need to be run. There is a file called `__init__.py` to indicate to Python that this folder is a package so the modules in here can be imported with `from Library import xyz.py`. Three of the files in this folder (`UltrasonicRanging.py`, `SenseLED.py`, and `Keypad.py`) have been copied over from the [Freenove Ultimate Starter Kit for Raspberry Pi repository on GitHub.](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi) All three of these files include author information at the beginning. The rest of the files have been created by us and are thoroughly commented.

## public
This folder includes all the public resources, such as the JavaScript files.
