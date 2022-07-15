import RPi.GPIO as GPIO
import time

buzzerPin = 4 # This is the actual pin the buzzer is connected to
def setup():
	GPIO.setmode(GPIO.BCM)        # use ordered GPIO Numbering
	GPIO.setup(buzzerPin, GPIO.OUT)    # set buzzerPin to OUTPUT mode

# This function turns on and off the buzzer repeatedly 10 times with 0.2 sec in between.
def emergencyAlarm():
	setup()
	for x in range(10):
		GPIO.output(buzzerPin, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(buzzerPin, GPIO.LOW)
		time.sleep(0.2)

if __name__ == "__main__":
	try:
		emergencyAlarm()
	except KeyboardInterrupt:  # Press ctrl-c to end the program.
		GPIO.cleanup()