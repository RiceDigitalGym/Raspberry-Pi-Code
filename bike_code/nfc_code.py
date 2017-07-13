"""
Code to read RFID Tags for Raspberry Pi and send them to the database.

Authors:
Aidan Curtis
Carl Henderson Feb 2017
Hamza Nauman   June 2017
Titus Deng     July 2017
"""

import util_functions
import nfc
import requests
import json
import signal

logger = util_functions.get_logger("NFC")

global clf


def sigint_handler(*args):
    """
    Signal Handler that is executed whenever the user presses CTRL-C on the terminal
    or when a SIGINT signal is sent to the program.
    """
    print "\nNFC Sensor Disconnected"
    logger.info("NFC Sensor Disconnected")
    raise SystemExit  # Exit program after printing statement.


def connected(tag):
    print ("\nTag Name: " + str(tag))
    return False


def main():

    global clf

    while True:
        API_PROCESS_ENDPOINT = "http://52.34.141.31:8000/bbb/process_tag"
        API_CHECKRPM_ENDPOINT = "http://52.34.141.31:8000/bbb/check_rpm"

        tag = clf.connect(rdwr={'on-connect': connected})

        # Extract the ID from the Tag object and convert it into an integer
        RFID = int("0x" + str(tag.identifier.encode("hex")), 16)
        # TODO: Add formatting to log messages
        logger.info("Tag scanned with RFID " + RFID)
        data = {"RFID": RFID, "serialNumber": util_functions.getserial()}
        try:
            r_process = requests.post(url=API_PROCESS_ENDPOINT, data=data)
            resp = json.loads(r_process.text)  # extracting response text
            print("Tag Status: %s" % resp["status"])
            r_checkRPM = requests.post(url=API_CHECKRPM_ENDPOINT, data=data)
            logger.debug("Data for tag with RFID " + RFID + " sent")
        except requests.exceptions.RequestException as e:
            print "ERROR: " + str(e)
            logger.exception("Data for Tag with RFID " + RFID + "could not be send")


if __name__ == "__main__":
    # Register the SIGINT handler for when CTRL-C is pressed by user
    signal.signal(signal.SIGINT, sigint_handler)

    clf = nfc.ContactlessFrontend('usb')
    print "NFC Sensor Connected"
    logger.info("NFC Sensor Connected")
    main()





