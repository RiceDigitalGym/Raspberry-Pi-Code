"""
Code to read RFID Tags for Rasp Pi

Carl Henderson Feb 2017
"""

import nfc
import time
import datetime
import requests
import urllib
import httplib


def connected(tag):
    print(tag);
    return False



def getserial():
	cpuserial = "0000000000000000"
	try:
		f = open('/proc/cpuinfo' , 'r')
		for line in f:
			if line[0:6] == 'Serial':
				cpuserial = line[10:26]
		f.close()
	except:
		cpuserial = "ERROR000000000"
	return int("0x" + cpuserial, 16)



clf = nfc.ContactlessFrontend('usb')

while True:
    #API_ENDPOINT = API_ENDPOINT = "digitalgym.cq4d8vjo7uoe.us-west-2.rds.amazonaws.com:3306" 
    API_ENDPOINT = API_ENDPOINT = "http://52.34.141.31:8000/bbb/process_tag"
    API_KEY = "ashu1234"

    tag = clf.connect(rdwr={'on-connect': connected})
    data = {"tag": tag, "bikeId": getserial()}
    try:
        r = requests.post(url=API_ENDPOINT, data=data)
    except requests.exceptions.RequestException as e:
        print e



    # extracting response text
    pastebin_url = r.text
    print("the pastebin URL is: %s" % pastebin_url)

