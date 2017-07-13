#!/bin/bash
# A script that runs the bike_code processes.

sudo killall python >nul 2>&1
sudo python ./bike_code/alert.py &
sudo python ./bike_code/nfc_code.py &
sudo python ./bike_code/rpm_sensor.py &&
pkill alert
pkill nfc_code
