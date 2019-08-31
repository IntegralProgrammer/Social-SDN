#!/bin/bash

tcp_port=$(zenity --entry --text="Enter the TCP Port to listen on." --title="TCP to UNIX")
unix_socket=$(zenity --file-selection --title="Select the UNIX-Domain socket to connect to...")

#Start the socat relay
socat TCP-LISTEN:$tcp_port,fork UNIX-CONNECT:$unix_socket &
socat_pid=$!

#Wait until we want to stop
zenity --info --text="<span size='xx-large'>Forwarding 0.0.0.0:$tcp_port to $unix_socket</span>" --title="Socat GUI" --ok-label="STOP"
kill $socat_pid
