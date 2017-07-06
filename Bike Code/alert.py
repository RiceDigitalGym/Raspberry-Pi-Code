import smtplib
from email.mime.text import MIMEText
import time
import signal
import json
import serial
import requests

# API endpoint for testing connection with backend.
API_TEST_CONNECTION = "http://52.34.141.31:8000/bbb/test_connection"

me = "digital.gym.alert@gmail.com"            # Email address for sender
target = "hn9@rice.edu"                       # Email address for recipient
server = smtplib.SMTP("smtp.gmail.com", 587)  # Initiate Email Server
serial_num = serial.getserial()               # Serial Number of bike this code is running on
# serial_num = "12345"

global error  # Global variable indicating whether there is an error currently


def sigint_handler(*args):
    """
    Signal Handler that is executed whenever the user presses CTRL-C on the terminal
    or when a SIGINT signal is sent to the program.
    """
    print "\nAlert Stopped"
    raise SystemExit


def main():
    global error

    error = False  # No error initially

    print "Alert Started"

    while True:
        time.sleep(10)  # Recheck connection with server every 10 seconds
        try:
            resp = requests.get(API_TEST_CONNECTION)  # Test Connection
            print json.loads(resp.text)["status"]  # Should be "success" if connection established

            # If there was previously an error, erase it and send an email signifying that
            # the connection with the server has been restored.
            if error:
                error = False
                send_email("Restored")

        except requests.exceptions.RequestException as e:
            print e
            # If there wasn't previously an error, create it and send an email signifying that
            # the connection with the server has failed.
            if not error:
                error = True
                send_email("Failed")


def send_email(event):
    """
    Sends an email to the target email specifying the time and date of "event".
    """
    now_date = time.strftime("%x")  # Current Date
    now_time = time.strftime("%X")  # Current Time

    # Main text of email.
    data = event + " Date: " + now_date + "\n" + \
        event + " Time: " + now_time + "\n"

    msg = MIMEText(data)

    msg["Subject"] = "Connection " + event + " on Bike Serial #" + str(serial_num)
    msg["From"] = me
    msg["To"] = target

    server.sendmail(me, target, msg.as_string())


if __name__ == "__main__":
    server.starttls()
    server.login(me, "ashu1234")  # Login into sender email address
    signal.signal(signal.SIGINT, sigint_handler)  # Register SIGINT handler
    main()
