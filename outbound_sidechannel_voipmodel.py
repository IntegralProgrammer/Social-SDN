#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

last_packet_time = None
inCall = False
packet_counter = 0
start_time_unix = time.time()
min_packet_time_spacing = None
max_packet_time_spacing = None
def process_packet(receiver, plaintext_payload):
	global last_packet_time
	global inCall
	global packet_counter
	global start_time_unix
	global min_packet_time_spacing
	global max_packet_time_spacing
	now_time_ms = int(time.time() * 1000)
	
	#All outbound packets should be padded to (8 timestamp bytes) + (2 length bytes) + (1600 payload bytes) = (1610 total bytes)
	if len(plaintext_payload) > 1600:
		raise Exception("I don't know what to do with this large packet.")
	
	packet_counter += 1
	now_time_unix = time.time()
	if inCall:
		packet_time_spacing = now_time_unix - last_packet_time
		last_packet_time = time.time()
		if min_packet_time_spacing is None:
			min_packet_time_spacing = packet_time_spacing
		
		if max_packet_time_spacing is None:
			max_packet_time_spacing = packet_time_spacing
		
		if packet_time_spacing < min_packet_time_spacing:
			min_packet_time_spacing = packet_time_spacing
			sys.stderr.write("Packet Time Spacing: MIN={}, MAX={}\n".format(min_packet_time_spacing, max_packet_time_spacing))
		
		if packet_time_spacing > max_packet_time_spacing:
			max_packet_time_spacing = packet_time_spacing
			sys.stderr.write("Packet Time Spacing: MIN={}, MAX={}\n".format(min_packet_time_spacing, max_packet_time_spacing))
		
	if (now_time_unix - start_time_unix) > 15:
		packets_per_second = float(packet_counter) / float(now_time_unix - start_time_unix)
		packet_counter = 0
		start_time_unix = now_time_unix
		sys.stderr.write("Outbound data rate is: {} Packets/Second.\n".format(packets_per_second))
		if packets_per_second > 40 and not inCall:
			inCall = True
			last_packet_time = time.time()
			sys.stderr.write("\tCall has started\n")
	
	return now_time_ms.to_bytes(8, byteorder='big') + len(plaintext_payload).to_bytes(2, byteorder='big') + plaintext_payload + bytes(1600 - len(plaintext_payload))
