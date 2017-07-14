"""
Code to compute the RPM of the bike, and send it to the server. Also handles session creation and end through
pedalling.

Authors:
Aidan Curtis
Hamza Nauman July 2017

"""
import util_functions
import RPi.GPIO as GPIO
import time
import json
import requests
import signal

global first        # Boolean to indicate if next RPM will be the first of a new workout
global last_time    # Time in seconds of the last time the pedal crossed the Hall Effect sensor
global miss         # Integer to keep track of time since last RPM. Incremented by 1 every 2 seconds.

# Define the API endpoint:
API_ENDPOINT = "http://52.34.141.31:8000/bbb/bike"
API_START_WORKOUT = "http://52.34.141.31:8000/bbb/start_workout"
API_END_WORKOUT = "http://52.34.141.31:8000/bbb/end_workout"

logger = util_functions.get_logger("RPM")


def sigint_handler(*args):
    """
    Signal Handler that is executed whenever the user presses CTRL-C on the terminal
    or when a SIGINT signal is sent to the program.
    """
    GPIO.cleanup()  # Clean up ports being used to prevent damage.
    if not first:   # If a workout already exists, end it before exiting.
        end_workout()
    print "\nRPM Sensor Disconnected"
    logger.info("RPM Sensor Disconnected")
    raise SystemExit


def sensor_callback(channel):
    """
    This function is function that is called when the Hall Effect sensor is triggered
    """
    global first
    global last_time
    global miss

    # If its the first RPM of a new workout, create a new session
    if first:
        start_workout()
        first = False

    miss = 0
    if not last_time:
        last_time = time.time()

    current_time = time.time()

    rpm = (1 / (current_time - last_time)) * 60

    if 200 > rpm > 10:
        print "Rpm: " + str(int(rpm))
        post_data = {"rpm": rpm, "serialNumber": util_functions.getserial()}
        try:
            r = requests.post(url=API_ENDPOINT, data=post_data)
            print "RPM Status: " + json.loads(r.text)["status"]
            logger.debug("RPM of " + str(rpm) + " collected and sent to the server")
        except requests.exceptions.RequestException as error:
            logger.exception("RPM data could not be sent to the server")
            print error

    last_time = current_time


def start_workout():
    """
    Sends a request to the backend to start a workout session on the current bike if one doesnt already exist.
    """
    try:
        post_data = {"serialNumber": util_functions.getserial()}
        r = requests.post(url=API_START_WORKOUT, data=post_data)
        print "Start workout status: " + json.loads(r.text)["status"]
        logger.info("Start Workout request sent with status: " + json.loads(r.text)["status"])
    except requests.exceptions.RequestException as error:
        logger.exception("Start workout request could not be sent to the server")
        print error


def end_workout():
    """
    Sends a request to the backend to the current workout session on the current bike if one exists.
    """
    try:
        post_data = {"serialNumber": util_functions.getserial()}
        r = requests.post(url=API_END_WORKOUT, data=post_data)
        print "End workout status: " + json.loads(r.text)["status"]
        logger.info("End Workout request sent with status: " + json.loads(r.text)["status"])
    except requests.exceptions.RequestException as error:
        logger.exception("End workout request could not be sent to the server")
        print error


def main():
    global first
    global miss

    first = True  # No workout exists when code starts
    miss = 0

    #  Keep printing a zero RPM every 2 seconds of inactivity for 30 seconds when session is active. Then end session.
    while True:
        miss += 1
        time.sleep(2)
        if 1 < miss < 15:
            print "Rpm: 0"
        if miss == 15 and not first:  # If session exists and 30 seconds have elapsed.
            end_workout()
            first = True


if __name__ == "__main__":
    try:
        # Register the SIGINT handler for when CTRL-C is pressed by user
        signal.signal(signal.SIGINT, sigint_handler)
    except:
        logger.exception("Could not configure SIGINT handler")
        raise
        
    try:
        GPIO.setmode(GPIO.BCM)
        # Set switch GPIO as input
        GPIO.setup(27, GPIO.IN)
        GPIO.add_event_detect(27, GPIO.FALLING, callback=sensor_callback)
        print("RPM Sensor Connected")
        logger.info("RPM Sensor Connected")
    except:
        logger.exception("Could not configure RPM Sensor properly")
        raise

    last_time = 0
    main()
