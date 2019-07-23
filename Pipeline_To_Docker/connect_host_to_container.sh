#!/bin/bash

CONTAINER_ID=$1

cat netpipe | sudo socat -d -d STDIO TUN:192.168.4.1/24,tun-name=tun0,up | (cd host_side && python3 outbound_gatekeeper.py) | (cd container_side && python3 inbound_gatekeeper.py) | sudo ./connect_container_to_pipe.sh $CONTAINER_ID | (cd container_side && python3 outbound_gatekeeper.py) | (cd host_side && python3 inbound_gatekeeper.py) > netpipe
