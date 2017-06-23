"""
Code to read RFID Tags for Rasp Pi
Carl Henderson Feb 2017
"""

import serial
import nfc
import requests
import json
import signal
import urllib
import httplib
import time
import datetime


def sigint_handler(*args):
    """
    Signal Handler that is executed whenever the user presses CTRL-C on the terminal
    or when a SIGINT signal is sent to the program.
    """
    print "NFC Sensor Disconnected"
    raise SystemExit  # Exit program after printing statement.


def connected(tag):
    print ("\nTag Name: " + str(tag))
    return False

clf = nfc.ContactlessFrontend('usb')
print "NFC Sensor Connected"

# Register the SIGINT handler for when CTRL-C is pressed by user
signal.signal(signal.SIGINT, sigint_handler)

while True:
    API_ENDPOINT = "http://52.34.141.31:8000/bbb/process_tag"

    tag = clf.connect(rdwr={'on-connect': connected})

    # Extract the ID from the Tag object and convert it into an integer
    RFID = int("0x" + str(tag.identifier.encode("hex")), 16)
    data = {"RFID": RFID, "serialNumber": serial.getserial()}
    try:
        r = requests.post(url=API_ENDPOINT, data=data)
        resp = json.loads(r.text)  # extracting response text
        print("Tag Status: %s" % resp["status"])
    except requests.exceptions.RequestException as e:
        print "ERROR: " + str(e)





