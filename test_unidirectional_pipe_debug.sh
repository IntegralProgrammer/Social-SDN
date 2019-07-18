#!/bin/bash
sudo socat -d -d STDIO TUN:192.168.3.10/24,tun-name=tun0,up | python3 outbound_gatekeeper.py | python3 debugger_passthrough.py | python3 inbound_gatekeeper.py | sudo socat -d -d STDIO TUN:192.168.1.1/24,tun-name=tun1,up > /dev/null
