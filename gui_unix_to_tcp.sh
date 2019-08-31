#!/bin/bash

ip_port=$(zenity --entry --text="Enter the IP:PORT of the service to connect to." --title="UNIX to TCP")
unix_socket=$(zenity --file-selection --save --title="Select the UNIX-Domain socket to listen on...")

#Start the socat relay
socat UNIX-LISTEN:$unix_socket,fork TCP-CONNECT:$ip_port &
socat_pid=$!

#Wait until we want to stop
zenity --info --text="<span size='xx-large'>Listening on $unix_socket</span>" --title="Socat GUI" --ok-label="STOP"
kill $socat_pid
