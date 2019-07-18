#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json

import umsgpack
import nacl.secret
from scapy.all import IP
from SocatAdapter3 import SocatParser

PUBLIC_KEY_FILE = "service_publickey.json"
KEYMAPPINGS_FILE = "tx_keymappings.json"
IPMAPPINGS_FILE = "tx_ipmappings.json"

f_public_key = open(PUBLIC_KEY_FILE)
localdb_service_publickey = bytes.fromhex(str(json.loads(f_public_key.read())))
f_public_key.close()

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
	localdb_ipmappings[ipmappings[key]] = bytes.fromhex(key)

#unique crypto_nonce variable for each client
localdb_crypto_nonces = {}
for key in keymappings:
	localdb_crypto_nonces[bytes.fromhex(key)] = 0

parser_obj = SocatParser()
while True:
	byte = sys.stdin.buffer.read(1)
	ret = parser_obj.addByte(ord(byte))
	if ret is not None:
		#sys.stderr.write("Passing: {}\n".format(ret.summary()))
		
		outbound_msg = []
		#Assign the appropriate source public key (this is a constant)
		ret.src = "0.0.0.0"
		outbound_msg.append(localdb_service_publickey)
		
		#Assign the appropriate destination public key (this is a function of the destination IP address)
		if ret.dst not in localdb_ipmappings:
			continue
		
		dst_publickey = localdb_ipmappings[ret.dst]
		encryption_box = localdb_naclboxes[dst_publickey]
		crypto_nonce = localdb_crypto_nonces[dst_publickey]
		ret.dst = "0.0.0.0"
		
		outbound_msg.append(dst_publickey)
		
		#Use an appropriate nonce
		outbound_payload = encryption_box.encrypt(bytes(ret), nonce=crypto_nonce.to_bytes(24, byteorder='big'))
		crypto_nonce += 1
		localdb_crypto_nonces[dst_publickey] = crypto_nonce
		
		#Serialize the packet
		outbound_msg.append(outbound_payload)
		
		#Send it down the pipe
		sys.stdout.buffer.write(umsgpack.packb(outbound_msg))
		sys.stdout.buffer.flush()
