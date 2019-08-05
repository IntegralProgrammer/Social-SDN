#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import nacl.public

HOMEDIR = os.environ['HOME']

sk = nacl.public.PrivateKey.generate()
pk = sk.public_key

f_sk = open(HOMEDIR + "/.socialsdn/privkey.hex", 'w')
f_sk.write(bytes(sk).hex())
f_sk.close()
os.chmod(HOMEDIR + "/.socialsdn/privkey.hex", 256) #Read only by user

f_pk = open(HOMEDIR + "/.socialsdn/pubkey.hex", 'w')
f_pk.write(bytes(pk).hex())
f_pk.close()
os.chmod(HOMEDIR + "/.socialsdn/pubkey.hex", 256) #Read only by user
