"""
Code to read RFID Tags for Rasp Pi
test1
Carl Henderson Feb 2017
"""

import serial
import nfc
import time
import datetime
import requests
import urllib
import httplib
import json


def connected(tag):
    print ("Tag: " + str(tag))
    return False

clf = nfc.ContactlessFrontend('usb')
print "NFC Sensor Connected"

while True:
    API_ENDPOINT = "http://52.34.141.31:8000/bbb/process_tag"

    tag = clf.connect(rdwr={'on-connect': connected})

    if (tag == False):
        print "\nNFC Sensor Disconnected"
        break

    # Extract the ID from the Tag object and convert it into an integer
    RFID = int("0x" + str(tag.identifier.encode("hex")), 16)
    data = {"RFID": RFID, "serialNumber": serial.getserial()}
    try:
        r = requests.post(url=API_ENDPOINT, data=data)
        # extracting response text
        resp = json.loads(r.text)
        print("Status: %s" % resp["status"])
    except requests.exceptions.RequestException as e:
        print "ERROR: " + str(e)





