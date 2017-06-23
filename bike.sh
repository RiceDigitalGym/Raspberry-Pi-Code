#!/bin/bash
# A script that runs the bike_code processes.

sudo python ./nfc_code & sudo python ./rpm_sensor && killall -9 rpm_sensor
