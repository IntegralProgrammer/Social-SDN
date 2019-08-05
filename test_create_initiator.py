#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

import nacl.utils

from create_container_config import create_protected_initiator_container_config, get_our_identity_hex
from transport_mechanisms import transport_mechanisms

transport_mech_name = input("Enter the transport mechanism name: ")
transport_mech_args = []
for arg in transport_mechanisms[transport_mech_name].getInitiatorArgs():
	transport_mech_args.append(arg[1](input("Enter a value for ({}): ".format(arg[0]))))

transport_mech = {}
transport_mech['name'] = transport_mech_name
transport_mech['initiator_args'] = transport_mechanisms[transport_mech_name].resolveInitiatorArgs(transport_mech_args)
transport_mech['connector_args'] = transport_mechanisms[transport_mech_name].resolveConnectorArgs(transport_mech_args)

remote_peer_id = input("Enter the remote peer ID: ")

tx_symmetric_key = nacl.utils.random().hex()
rx_symmetric_key = nacl.utils.random().hex()

this_ipaddr = input("Enter the IP address for this side: ")
remote_ipaddr = input("Enter the IP address for the remote side: ")
app_name = input("Enter the app name: ")
sc_protectors = []

current_time = int(time.time())
nacl_nonce = current_time.to_bytes(24, byteorder='big')

prot_remote_config_req = create_protected_initiator_container_config(transport_mech, remote_peer_id, tx_symmetric_key, rx_symmetric_key, this_ipaddr, remote_ipaddr, app_name, sc_protectors, nacl_nonce)

#Get our own ID
our_id = get_our_identity_hex()
print(our_id + prot_remote_config_req.hex())
