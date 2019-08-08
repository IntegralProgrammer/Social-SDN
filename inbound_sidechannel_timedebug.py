#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys

packet_counter = 0
cumulative_delay = 0.0
min_delay = None
max_delay = None
def process_packet(sender, plaintext_payload):
	global packet_counter
	global cumulative_delay
	global min_delay
	global max_delay
	
	now_time_ms = int(time.time() * 1000)
	remote_time_ms = int.from_bytes(plaintext_payload[0:8], byteorder='big')
	timediff = abs(now_time_ms - remote_time_ms)
	
	if min_delay is None:
		min_delay = timediff
	
	if max_delay is None:
		max_delay = timediff
	
	if timediff < min_delay:
		min_delay = timediff
	
	if timediff > max_delay:
		max_delay = timediff
	
	cumulative_delay += timediff
	packet_counter += 1
	if packet_counter == 250:
		avg_delay = cumulative_delay / 250.0
		sys.stderr.write("For last 250 packets, delay statistics are - MIN: {}ms, MAX: {}ms, AVG: {}ms.\n".format(min_delay, max_delay, avg_delay))
		packet_counter = 0
		cumulative_delay = 0.0
		min_delay = None
		max_delay = None
	
	return plaintext_payload[8:]
