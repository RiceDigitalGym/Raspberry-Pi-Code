#!/bin/bash
# A script reboots the pi when it has made too many attemps to restore wifi

sudo killall python >nul 2>&1
echo "prepare to reboot"
sleep 10
sudo reboot
