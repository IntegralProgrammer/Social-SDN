#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import socket
import time
import random
import json

def getServerPubkey():
	f_map = open("rx_ipmappings.json", 'r')
	ip_map = json.loads(f_map.read())
	f_map.close()
	for k in ip_map:
		if ip_map[k] == '192.168.1.1':
			return k
	return None

random.seed(time.time())

HOMEDIR = os.environ['HOME']
TIMEDIFFS_DIR = HOMEDIR + "/.socialsdn/timediffs/"

SERVER_ADDRESS = ('192.168.1.1', 3950)
UDPSOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

beginTime = time.time()

#Send a TIME_REQUEST over to the server
#...TIME_REQUEST is defined as [0 (1 byte), pseudorandom value (8 bytes), 0 (8 bytes)]
time_req = bytes([0])
pseudorandom_val = []
for i in range(8):
	pseudorandom_val.append(random.randint(0,255))
time_req += bytes(pseudorandom_val)
time_req += bytes(8)

UDPSOCK.sendto(time_req, SERVER_ADDRESS)

#Wait for the TIME_RESPONSE from the remote server
#...TIME_RESPONSE is defined as [1 (1 byte), pseudorandom value (8 bytes), UNIX time in milliseconds (8 bytes)]
time_resp, srv = UDPSOCK.recvfrom(1024)

if len(time_resp) < 17:
	raise Exception("Packet length too short")

if time_resp[0] != 1:
	raise Exception("Not a time response packet")

if time_resp[1:9] != bytes(pseudorandom_val):
	raise Exception("Pseudorandom value does not match")

remote_unix_time_ms = int.from_bytes(time_resp[9:17], byteorder='big')

totalTime = time.time() - beginTime
if totalTime > 3.0:
	raise Exception("Network delay too large. Unable to read remote time.")
else:
	sys.stderr.write("Saving the time difference between this host and the remote host.\n")
	timediff = int(beginTime * 1000) - remote_unix_time_ms
	sys.stderr.write("LOCAL_TIME - REMOTE_TIME = {} ms.\n".format(timediff))
	
	#Save timediff to a file/database
	server_id = getServerPubkey()
	if server_id is None:
		raise Exception("Something is wrong with rx_ipmappings.json")
	
	f_save = open(TIMEDIFFS_DIR + server_id + ".json", 'w')
	f_save.write(json.dumps(timediff))
	f_save.close()
	sys.stderr.write("Recorded the time difference...Done.\n")
