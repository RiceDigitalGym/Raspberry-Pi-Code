# Import required libraries
import serial
import RPi.GPIO as GPIO
import time
import json
import requests
import signal
import datetime
import urllib
import httplib
import smtplib
from email.mime.text import MIMEText

global last_time
global miss

# Define the API endpoint:
API_ENDPOINT = "http://52.34.141.31:8000/bbb/bike"
API_SESSION_CHECK = "http://52.34.141.31:8000/bbb/sessionlisten"
API_LOG_OUT = "http://52.34.141.31:8000/bbb/logout"


def sigint_handler(*args):
    """
    Signal Handler that is executed whenever the user presses CTRL-C on the terminal
    or when a SIGINT signal is sent to the program.
    """
    GPIO.cleanup()  # Clean up ports being used to prevent damage.
    print "\nRPM Sensor Disconnected"
    raise SystemExit


def sensor_callback(channel):
    """
    This function is function that is called when the Hall Effect sensor is triggered
    """
    global last_time
    global miss

    miss = 0
    if not last_time:
        last_time = time.time()

    current_time = time.time() 

    if (1 / (current_time - last_time)) * 60 < 200:
        if (1 / (current_time - last_time)) * 60 > 10:
            rpm = (1 / (current_time - last_time)) * 60
            print "Rpm: " + str(int(rpm))
            post_data = {"rpm": rpm, "serialNumber": serial.getserial()}
            try:
                r = requests.post(url=API_ENDPOINT, data=post_data)
                print json.loads(r.text)["status"]
            except requests.exceptions.RequestException as error:
                print error

        last_time = current_time


def main():
    global miss

    miss = 0

    """
    This following try catch is for positing zeros if the hall effect is  not triggered
    """
    while True:
        if miss < 15:
            miss += 1
            time.sleep(2)
            if miss > 1:
                print "Rpm: 0"



GPIO.setmode(GPIO.BCM)

print("Setup of GPIO pin as Input for RPM Sensor")

# Set switch GPIO as input

GPIO.setup(27, GPIO.IN)
GPIO.add_event_detect(27, GPIO.FALLING, callback=sensor_callback)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)  # Register SIGINT handler
    last_time = 0
    main()
