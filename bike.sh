#!/bin/bash
# A script that runs the bike_code processes.

sudo python ./Bike\ Code/alert.py &
sudo python ./Bike\ Code/nfc_code.py &
sudo python ./Bike\ Code/rpm_sensor.py &&
pkill alert
pkill nfc_code
