"""
Code to read RFID Tags for Rasp Pi
test2
Carl Henderson Feb 2017
"""

import serial
import nfc
import time
import datetime
import requests
import urllib
import httplib


def connected(tag):
    print(tag);
    return False

clf = nfc.ContactlessFrontend('usb')

while True:
    #API_ENDPOINT = API_ENDPOINT = "digitalgym.cq4d8vjo7uoe.us-west-2.rds.amazonaws.com:3306" 
    API_ENDPOINT = API_ENDPOINT = "http://0.0.0.0:8000/bbb/process_tag"
    API_KEY = "ashu1234"

    tag = clf.connect(rdwr={'on-connect': connected})
    data = {"tag": tag, "machineID": serial.getserial()}
    try:
        r = requests.post(url=API_ENDPOINT, data=data)
    except requests.exceptions.RequestException as e:
        print e



    # extracting response text
    pastebin_url = r.text
    print("the pastebin URL is: %s" % pastebin_url)

