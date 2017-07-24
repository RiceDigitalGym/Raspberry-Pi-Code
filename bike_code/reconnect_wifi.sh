#!/bin/bash
# A script that disconnect and reconnect wifi when the Pi's connection to the server is lost

nmcli radio wifi off 
nmcli radio wifi on 
echo "wifi on"
