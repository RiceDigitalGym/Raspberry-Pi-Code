"""
Code to send an email to notify after the RaspberryPi is rebooted.
"""

import time
import smtplib
import util_functions
from email.mime.text import MIMEText

me = "digital.gym.alert@gmail.com"            # Email address for sender
target = "haleyko@rice.edu"                       # Email address for recipient
server = smtplib.SMTP("smtp.gmail.com", 587)  # Initiate Email Server
logger = util_functions.get_logger("Alert")
serial_num = util_functions.getserial()               # Serial Number of bike this code is running on
event = "Reboot"


def send_email(event):
    """
    Sends an email to the target email specifying the time and date after the RaspberryPi rebooted.
    """
    now_date = time.strftime("%x")  # Current Date
    now_time = time.strftime("%X")  # Current Time

    # Main text of email.
    data = event + " Date: " + now_date + "\n" + \
        event + " Time: " + now_time + "\n"

    msg = MIMEText(data)

    msg["Subject"] = "Bike Serial #" + str(serial_num) + event
    msg["From"] = me
    msg["To"] = target

    try:
        server.starttls()
        server.login(me, "ashu1234")  # Login into sender email address"
        server.sendmail(me, target, msg.as_string())
        logger.info("Sent email for event: \'" + event + "\'")
        server.quit()
    except smtplib.SMTPException:
        logger.exception("Failed to send email for event: \'" + event + "\'")

send_email(event)
