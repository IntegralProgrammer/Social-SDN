#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

def process_packet(receiver, plaintext_payload):
	now_time_ms = int(time.time() * 1000)
	return now_time_ms.to_bytes(8, byteorder='big') + plaintext_payload
