"""
Code to send an email to notify after the RaspberryPi is rebooted.
"""

import util_functions

logger = util_functions.get_logger("Reboot")
serial_num = str(util_functions.getserial())  # Serial Number of bike this code is running on
event = "Reboot"


def send_reboot_email():
    """
    Sends an email to the target email specifying the time and date after the RaspberryPi rebooted.
    """
    util_functions.send_event_email(
        event,
        "Bike Serial #" + serial_num + " rebooted",
        logger
    )

if __name__ == "__main__":
    send_reboot_email()
