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
