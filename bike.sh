#!/bin/bash
# A script that runs the bike_code processes.

sudo python ./Bike\ Code/nfc_code & sudo python ./Bike\ Code/rpm_sensor && killall -9 rpm_sensor
