#!/bin/bash
# A script that disconnect and reconnect wifi when the Pi's connection to the internet is lost

wget -q --spider http://www.google.com

if [[ $? -eq 0 ]]; then
    echo "wifi is on"

else
    nmcli radio wifi off 
    nmcli radio wifi on 
    echo "wifi back on"

fi

