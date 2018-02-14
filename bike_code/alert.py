"""
Code to periodically check connection with the backend server, and send emails to notify when the connection is
down or up again.

Authors:
Hamza Nauman July 2017

"""
import smtplib
from email.mime.text import MIMEText
import time
import signal
import json
import util_functions
import requests
import subprocess

# API endpoint for testing connection with backend.
API_TEST_CONNECTION = "http://54.67.95.108:8000/bbb/test_connection"

logger = util_functions.get_logger("Alert")
serial_num = str(util_functions.getserial())          # Serial Number of bike this code is running on
# serial_num = "12345"

global num_atmp    # Count the number of attemps the pi tries to restore wifi connection

global error  # Global variable indicating whether there is an error currently


def sigint_handler(*args):
    """
    Signal Handler that is executed whenever the user presses CTRL-C on the terminal
    or when a SIGINT signal is sent to the program.
    """
    print "\nAlert Stopped"
    logger.info("Connection Status Alert Stopped")
    raise SystemExit


def main():
    global error

    error = False  # No error initially

    num_atmp = 0  # No attempt initially

    print "Alert Started"
    logger.info("Connection Status Alert Activated")

    post_data = {"serialNumber": serial_num}

    while True:
        time.sleep(60)  # Recheck connection with server every 10 seconds
        try:
            resp = requests.post(url=API_TEST_CONNECTION, data=post_data)  # Test Connection
            status = json.loads(resp.text)["status"]  # Should be "success" if connection established
            print "Ping Status: " + status
            logger.debug("Connection attempt to server successful with status: " + status)

            # If there was previously an error, erase it and send an email signifying that
            # the connection with the server has been restored.
            if error:
                error = False
                logger.info("Connection to server restored")
                send_alert_email("Restored")
                num_atmp = 0

        except requests.exceptions.RequestException as e:
            print e
            logger.debug("Connection attempt to server failed")
            # If there wasn't previously an error, create it and send an email signifying that
            # the connection with the server has failed.
            if num_atmp >= 4 :
                num_atmp = 0
                subprocess.call(["./bike_code/reboot.sh"])
            if not error:
                error = True
                logger.error("No Connection to server")
                try:
                    subprocess.call(["./bike_code/reconnect_wifi.sh"])
                    time.sleep(120)
                    num_atmp += 1
                except:
                    logger.exception("Failed to restart WIFI")
                    raise
                send_alert_email("Failed")
            

def send_alert_email(status):
    """
    Sends an email to the target email specifying the time and date of failure/success.
    """
    util_functions.send_event_email(
        status,
        "Connection " + status + " on Bike Serial #" + serial_num,
        logger
    )


if __name__ == "__main__":
    try:
        # Register the SIGINT handler for when CTRL-C is pressed by user
        signal.signal(signal.SIGINT, sigint_handler)
    except:
        logger.exception("Could not configure SIGINT handler")
        raise

    main()
