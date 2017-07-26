"""
Code to send an email to notify after the RaspberryPi is rebooted.
"""

import util_functions
import requests
import json

logger = util_functions.get_logger("Reboot")
serial_num = str(util_functions.getserial())  # Serial Number of bike this code is running on
event = "Reboot"

API_REBOOT = "http://52.34.141.31:8000/bbb/reboot"


def send_reboot_email():
    """
    Sends an email to the target email specifying the time and date after the RaspberryPi rebooted.
    """
    util_functions.send_event_email(
        event,
        "Bike Serial #" + serial_num + " rebooted",
        logger
    )


def send_reboot_request():
    """
    Sends an HTTP request to the backend server after the Raspberry Pi reboots.
    """
    post_data = {"serialNumber": serial_num}
    try:
        resp = requests.post(url=API_REBOOT, data=post_data)
        status = json.loads(resp.text)["status"]
        print "Reboot Status: " + status
        logger.info("Reboot request sent to the server with status: " + status)
    except requests.exceptions.RequestException:
        logger.error("Reboot request failed to send to the server")


if __name__ == "__main__":
    send_reboot_email()
    send_reboot_request()
