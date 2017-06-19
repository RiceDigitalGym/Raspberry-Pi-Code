# Import required libraries
import serial
import RPi.GPIO as GPIO
import time
import json
import datetime
import requests
import urllib
import httplib
import smtplib
from email.mime.text import MIMEText

global last_time

# Define the API endpoint:
API_ENDPOINT = "http://52.34.141.31:8000/bbb/bike"
API_SESSION_CHECK = "http://52.34.141.31:8000/bbb/sessionlisten"
API_LOG_OUT = "http://52.34.141.31:8000/bbb/logout"

def sensorCallback1(channel):
    """
    This function is function that is called when the Hall Effect sensor is triggered
    """
    global last_time
    global miss
    global sessionid

    miss = 0
    if not last_time:
        last_time = time.time()

    current_time = time.time() 

    if (1 / (current_time - last_time)) * 60 < 200:
        if (1 / (current_time - last_time)) * 60 > 10:
            rpm = (1 / (current_time - last_time)) * 60
            print "Rpm:" + str(int(rpm))
            post_data = {"rpm": rpm, "bikeId": serial.getserial()}
            try:
                r = requests.post(url=API_ENDPOINT, data=post_data)
            except requests.exceptions.RequestException as error:
                print error

        last_time = current_time


def main():
    global miss
    global sessionid


    sessionid = -1
    miss = 0

    """
    This following try catch is for positing zeros if the hall effect is  not triggered
    """
    try:
        while True:
            if not (sessionid == -1) and miss == 20:
                print("Sessionid: "+str(sessionid))
                logout = requests.post(url=API_LOG_OUT, data={"userId": sessionid})
                sessionid = -1

            miss += 1
            time.sleep(5)
            if miss >= 3:
                data2 = {"rpm": 0, "bikeId": serial.getserial()}

                try:
                    if sessionid == -1:
                        session = requests.get(url=API_SESSION_CHECK)
                        data = json.loads(session.text)
                        miss=3

                    if data and not (data['status'] == "failure"):

                        r = requests.post(url=API_ENDPOINT, data=data2)
                        sessionid = data['user']['id']
                        # sessionid = session.user.id
                        # print "sesionid"
                        # print sessionid
                        print "0 Response Posted"

                    else:
                        print "0 Response NOT Posted"

                except requests.exceptions.RequestException as e:
                    print e

    except KeyboardInterrupt:
        GPIO.cleanup()


GPIO.setmode(GPIO.BCM)

print("Setup of GPIO pin as Input for RPM Sensor")

# Set switch GPIO as input

GPIO.setup(27, GPIO.IN)
GPIO.add_event_detect(27, GPIO.FALLING, callback=sensorCallback1)

if __name__ == "__main__":
    last_time = 0
    main()
