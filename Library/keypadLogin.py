import RPi.GPIO as GPIO
from Library import Keypad       #import module Keypad
ROWS = 4        # number of rows of the Keypad
COLS = 4        #number of columns of the Keypad
keys =  [   '1','2','3','A',    #key code
			'4','5','6','B',
			'7','8','9','C',
			'*','0','#','D'     ]
letters = ['A', 'B', 'C', 'D'] # This is used to differentiate the letter keys
# This following list is used to differentiate the number keys
numbers = ['1','2','3','4','5','6','7','8','9','0']

# Both of the following pins use BOARD as their numbering system, not BCD
rowsPins = [18,23,24,25]        #connect to the row pinouts of the keypad
colsPins = [10,22,27,17]        #connect to the column pinouts of the keypad

# This section of the code is taken directly from the provided Python code
keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    #create Keypad object
keypad.setDebounceTime(50)      #set the debounce time

# This is the method that immediately runs when the first webpage is loaded.
# It keeps getting the key input until one of the 4 users (A, B, C, or D)
# is selected.
def selectUser():
	# This variable is the condition for the while loop
	correct = 0
	while (not correct):
		# The getKey() method is defined in keypad.py and is used to decode
		# what key is pressed. It returns the charater.
		key = keypad.getKey()

		# This print statement is just for debugging purposes. The if statement
		# prevents printing blank lines to the output.
		if (key != keypad.NULL):
			print('Pressed Key: ' + key)
		
		# This stops the while loop when a letter has been pressed.
		if (key in letters):
			correct = 1
	return key

def getUserPin():
	print ('Getting user pin:')
	enteredPin = ''
	acceptingResponses = 1
	while (acceptingResponses):
		key = keypad.getKey()

		# This print statement is just for debugging purposes. The if statement
		# prevents printing blank lines to the output.
		if (key != keypad.NULL):
			print('Pressed Key: ' + key)

		# If the '*' key is pressed, the function will return -1 to indicate
		# the user wants to select another user.
		if (key == '*'):
			acceptingResponses = 0
			return '-1'

		# If the '#' key is pressed, the stored pin is erased so that the
		# user can start over, if they made a mistake.
		elif (key == '#'):
			enteredPin = ''
			print ('Pin entry reset')

		# If a number is pressed, that number will be appended to the end
		# of the enteredPin string.
		elif (key in numbers):
			enteredPin += key

			# This print statement is just for debugging purposes. The if
			# statement prevents printing blank lines to the output.
			if (enteredPin != ''):
				print ('Entered Pin: ' + enteredPin)

			# Since all pin numbers are set as 4 characters, this will
			# return the final pin number when it reaches 4 characters.
			if (len(enteredPin) == 4):
				acceptingResponses = 0
				return enteredPin


# The following code is only for testing the keypad. This is not related
# to the actual midterm.
def loop():
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    #create Keypad object
    keypad.setDebounceTime(50)      #set the debounce time
    while(True):
        key = keypad.getKey()       #obtain the state of keys
        if(key != keypad.NULL):     #if there is key pressed, print its key code.
            print ("You Pressed Key : %c "%(key))
            
if __name__ == '__main__':     #Program start from here
    print ("Program is starting ... ")
    try:
        loop()
    except KeyboardInterrupt:  #When 'Ctrl+C' is pressed, exit the program. 
        GPIO.cleanup()
