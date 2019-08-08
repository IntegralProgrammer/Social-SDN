#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
#import time

import umsgpack
import nacl.secret
import nacl.exceptions
from scapy.all import IP, UDP, TCP
from SocatAdapter3 import socat_format

import inbound_sidechannel_shaper

CONST_DST_IP_FILE = "dst_ip.json"
KEYMAPPINGS_FILE = "rx_keymappings.json"
IPMAPPINGS_FILE = "rx_ipmappings.json"

f_dst_ip = open(CONST_DST_IP_FILE, 'r')
CONST_DST_IP = json.loads(f_dst_ip.read())
f_dst_ip.close()

#Construct nacl.secret.SecretBox(KEY) objects for all allowed contacts
f_keymappings = open(KEYMAPPINGS_FILE, 'r')
keymappings = json.loads(f_keymappings.read())
f_keymappings.close()

localdb_naclboxes = {}
for key in keymappings:
	localdb_naclboxes[bytes.fromhex(key)] = nacl.secret.SecretBox(bytes.fromhex(keymappings[key]))


f_ipmappings = open(IPMAPPINGS_FILE, 'r')
ipmappings = json.loads(f_ipmappings.read())
f_ipmappings.close()

localdb_ipmappings = {}
for key in ipmappings:
	localdb_ipmappings[bytes.fromhex(key)] = ipmappings[key]

#unique expected_nonce variable for each client
localdb_expected_nonces = {}
for key in keymappings:
	localdb_expected_nonces[bytes.fromhex(key)] = 0

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
	
	#Decrypt msgpack_pkt with our private key
	sender = msgpack_pkt[0]
	receiver = msgpack_pkt[1]
	payload = msgpack_pkt[2]
	if sender not in localdb_naclboxes:
		continue
	
	decryption_box = localdb_naclboxes[sender]
	decryption_nonce = payload[0:24] #NaCl uses a 24 byte nonce
	
	#...assert that this nonce follows the correct order, to stop replay attacks
	numerical_nonce = int.from_bytes(decryption_nonce, byteorder='big')
	expected_nonce = localdb_expected_nonces[sender]
	if numerical_nonce != expected_nonce:
		continue
	
	#Assign the appropriate source IP (this is a function of the source public key)
	try:
		decrypted_payload = decryption_box.decrypt(payload)
		expected_nonce += 1
		localdb_expected_nonces[sender] = expected_nonce
	except nacl.exceptions.CryptoError:
		continue
	
	#If we cannot assign the appropriate source IP then this client should not be allowed to connect
	if sender not in localdb_ipmappings:
		continue
	
	#incoming_time = int.from_bytes(decrypted_payload[0:8], byteorder='big')
	
	#incoming_pkt = IP(decrypted_payload[8:])
	incoming_pkt = IP(inbound_sidechannel_shaper.process_packet(sender, decrypted_payload))
	
	incoming_pkt.src = localdb_ipmappings[sender]
	
	#Debug
	#timediff = abs(incoming_time - int(time.time() * 1000))
	#sys.stderr.write("Incoming packet delayed by {} ms.\n".format(timediff))
	
	#Assign the appropriate destination IP (this is a constant)
	incoming_pkt.dst = CONST_DST_IP
	
	#Recalculate the IPv4 checksum
	del incoming_pkt.chksum
	
	#If this carries a UDP packet recalculate the checksum from the new pseudoheader
	if incoming_pkt.haslayer(UDP):
		del incoming_pkt[UDP].chksum
	
	#If this carries a TCP packet recalculate the checksum from the new pseudoheader
	if incoming_pkt.haslayer(TCP):
		del incoming_pkt[TCP].chksum
	
	incoming_pkt = incoming_pkt.__class__(bytes(incoming_pkt))
	
	#Send it over to Socat
	sys.stdout.buffer.write(socat_format(incoming_pkt))
	sys.stdout.buffer.flush()
