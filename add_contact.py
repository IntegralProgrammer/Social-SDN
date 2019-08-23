#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

HOMEDIR = os.environ['HOME']

userinfo = {}

userinfo['name'] = input("Enter the contact's name: ")
userinfo['pubkey'] = input("Enter the contact's public key: ")

#Validate pubkey
for c in userinfo['pubkey']:
	if c not in '0123456789abcdef':
		raise Exception("Public key contains invalid symbols!")

if len(userinfo['pubkey']) != 64:
	raise Exception("Public key is of invalid length!")

#Save the user's contact info
f = open(HOMEDIR + "/.socialsdn/contacts/" + userinfo['pubkey'] + ".json", 'w')
f.write(json.dumps(userinfo))
f.close()
