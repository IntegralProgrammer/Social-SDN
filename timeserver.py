#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import time

UDPSOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SERVER_ADDRESS = ('0.0.0.0', 3950)
UDPSOCK.bind(SERVER_ADDRESS)

#Wait for a TIME_REQUEST from the client
data, address = UDPSOCK.recvfrom(1024)

if len(data) < 17:
	raise Exception("Packet length too short")

if data[0] != 0:
	raise Exception("Not a time request packet")

pseudorandom_val = data[1:9]

#Send the current UNIX time back to the client
now_time_ms = int(time.time() * 1000)

resp_pkt = bytes([1])
resp_pkt += pseudorandom_val
resp_pkt += now_time_ms.to_bytes(8, byteorder='big')

UDPSOCK.sendto(resp_pkt, address)
