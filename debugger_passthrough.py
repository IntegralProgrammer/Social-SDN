#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import umsgpack

def validate_msgpacked(m_pkt):
	if type(m_pkt) == type([]):
		if len(m_pkt) == 3:
			if type(m_pkt[0]) == type(bytes()) and type(m_pkt[1]) == type(bytes()) and type(m_pkt[2]) == type(bytes()):
				return True
	return False

while True:
	#Read (and deserialize) an encrypted packet from STDIN
	msgpack_pkt = umsgpack.unpack(sys.stdin.buffer)
	
	if not validate_msgpacked(msgpack_pkt):
		continue
	
	sender = msgpack_pkt[0]
	receiver = msgpack_pkt[1]
	payload = msgpack_pkt[2]
	nonce = payload[0:24]
	sys.stderr.write("Packet of length {} bytes from {} to {}. NONCE = {}\n".format(len(payload), sender.hex(), receiver.hex(), nonce.hex()))
	
	#Keep the pipe moving along
	sys.stdout.buffer.write(umsgpack.packb(msgpack_pkt))
	sys.stdout.buffer.flush()
