#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import json
import sys

import easygui
import pyperclip
import nacl.utils

from create_container_config import create_protected_initiator_container_config, get_our_identity_hex
from transport_mechanisms import transport_mechanisms

HOMEDIR = os.environ['HOME']

TRANSPORT_MECHS = ["netcat", "ngrok"]
APP_LIST = ["TIMESYNC", "linphone"]

#Populate userlist
userlist = {}
contacts_files = os.listdir(HOMEDIR + "/.socialsdn/contacts/")
for filename in contacts_files:
	if not filename.endswith(".json"):
		continue
	f = open(HOMEDIR + "/.socialsdn/contacts/" + filename)
	userinfo = json.loads(f.read())
	f.close()
	userlist[userinfo['name']] = userinfo.copy()

#Select who we will be connecting to
remote_username = easygui.choicebox("Connect to:", "SocialSDN", list(userlist.keys()))
if remote_username is None:
	sys.exit()

#Choose a transport mechanism
t_mech_name = easygui.choicebox("Transport mechanism:", "SocialSDN", TRANSPORT_MECHS)
if t_mech_name is None:
	sys.exit()

#Get the argument values for constructing the transport mechanism
transport_mech_args = []
for arg in transport_mechanisms[t_mech_name].getInitiatorArgs():
	gui_arg_val = easygui.enterbox("Enter a value for ({}):".format(arg[0]), "SocialSDN")
	if gui_arg_val is None:
		sys.exit()
	transport_mech_args.append(arg[1](gui_arg_val))

transport_mech = {}
transport_mech['name'] = t_mech_name
transport_mech['initiator_args'] = transport_mechanisms[t_mech_name].resolveInitiatorArgs(transport_mech_args)
transport_mech['connector_args'] = transport_mechanisms[t_mech_name].resolveConnectorArgs(transport_mech_args)

#Setup remote_peer_id from the ~/.socialsdn/contacts directory
remote_peer_id = userlist[remote_username]['pubkey']

tx_symmetric_key = nacl.utils.random().hex()
rx_symmetric_key = nacl.utils.random().hex()

this_ipaddr = easygui.enterbox("Enter the IP address for this side:", "SocialSDN")
if this_ipaddr is None:
	sys.exit()

remote_ipaddr = easygui.enterbox("Enter the IP address for the remote side:", "SocialSDN")
if remote_ipaddr is None:
	sys.exit()

app_name = easygui.choicebox("Select app:", "SocialSDN", APP_LIST)
if app_name is None:
	sys.exit()

#TODO: Configure setup of side-channel protectors
sc_protectors = []

current_time = int(time.time())
nacl_nonce = current_time.to_bytes(24, byteorder='big')

prot_remote_config_req = create_protected_initiator_container_config(transport_mech, remote_peer_id, tx_symmetric_key, rx_symmetric_key, this_ipaddr, remote_ipaddr, app_name, sc_protectors, nacl_nonce)

#Get our own ID
our_id = get_our_identity_hex()
connection_share_link = our_id + prot_remote_config_req.hex()

#Copy to clipboard
pyperclip.copy(connection_share_link)

#Let the user know that everything worked out
easygui.msgbox("Successfully copied the connection request to the clipboard.", "SocialSDN")
