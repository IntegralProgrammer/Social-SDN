#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

import nacl.public

from transport_mechanisms import transport_mechanisms
from application_resolver import resolveAppName

HOMEDIR = os.environ['HOME']

def get_our_identity_hex():
	f_pubkey = open(HOMEDIR + "/.socialsdn/pubkey.hex", 'r')
	pubkey_hex = f_pubkey.read().rstrip()
	f_pubkey.close()
	return pubkey_hex

def json_write(obj, fname):
	f = open(fname, 'w')
	f.write(json.dumps(obj))
	f.close()

def pipeline_script_write(plist, fname):
	f = open(fname, 'w')
	f.write(" | ".join(plist))
	f.close()
	
	#Only this user should be able to READ and EXECUTE
	os.chmod(fname, 320)

def create_connector_container_config(transport_mech, remote_peer_id, tx_symmetric_key, rx_symmetric_key, this_ipaddr, remote_ipaddr, app_name, sc_protectors):
	#Create the dst_ip.json file
	json_write(this_ipaddr, "dst_ip.json")
	
	#Create the rx_ipmappings.json file
	json_write({remote_peer_id: remote_ipaddr}, "rx_ipmappings.json")
	
	#Create the rx_keymappings.json file
	json_write({remote_peer_id: rx_symmetric_key}, "rx_keymappings.json")
	
	#Create the service_publickey.json file
	f_pubkey = open(HOMEDIR + "/.socialsdn/pubkey.hex", 'r')
	pubkey_hex = f_pubkey.read().rstrip()
	f_pubkey.close()
	json_write(str(pubkey_hex), "service_publickey.json")
	
	#Create the tx_ipmappings.json file
	json_write({remote_peer_id: remote_ipaddr}, "tx_ipmappings.json")
	
	#Create the tx_keymappings.json file
	json_write({remote_peer_id: tx_symmetric_key}, "tx_keymappings.json")
	
	#Create the UNIX pipeline
	pipeline_list = []
	
	#...listen
	pipeline_list.append("cat netpipe")
	
	#Resolve the UNIX pipeline command for data transport
	transport_command = transport_mechanisms[transport_mech['name']].connector(*transport_mech['connector_args'])
	
	#...connect to the transport mechanism that links to the initiator
	pipeline_list.append(transport_command)
	
	#...translate crypto traffic to inbound IPv4 traffic
	pipeline_list.append("python3 inbound_gatekeeper.py")
	
	#Resolve application name...see if it's allowed
	resolved_app_name = resolveAppName(app_name, False)
	
	#...run the executable in a new network namespace
	pipeline_list.append("unshare -n -r ./connect_executable_to_pipe.sh {} {}/24".format(resolved_app_name, this_ipaddr))
	
	#...translate outbound IPv4 traffic to crypto traffic
	pipeline_list.append("python3 outbound_gatekeeper.py > netpipe")
	
	#Save
	pipeline_script_write(pipeline_list, "run_pipeline.sh")


def create_initiator_container_config(transport_mech, remote_peer_id, tx_symmetric_key, rx_symmetric_key, this_ipaddr, remote_ipaddr, app_name, sc_protectors):
	#Create the dst_ip.json file
	json_write(this_ipaddr, "dst_ip.json")
	
	#Create the rx_ipmappings.json file
	json_write({remote_peer_id: remote_ipaddr}, "rx_ipmappings.json")
	
	#Create the rx_keymappings.json file
	json_write({remote_peer_id: rx_symmetric_key}, "rx_keymappings.json")
	
	#Create the service_publickey.json file
	f_pubkey = open(HOMEDIR + "/.socialsdn/pubkey.hex", 'r')
	pubkey_hex = f_pubkey.read().rstrip()
	f_pubkey.close()
	json_write(str(pubkey_hex), "service_publickey.json")
	
	#Create the tx_ipmappings.json file
	json_write({remote_peer_id: remote_ipaddr}, "tx_ipmappings.json")
	
	#Create the tx_keymappings.json file
	json_write({remote_peer_id: tx_symmetric_key}, "tx_keymappings.json")
	
	#Create the UNIX pipeline
	pipeline_list = []
	
	#...listen
	pipeline_list.append("cat netpipe")
	
	#Resolve the UNIX pipeline command for data transport
	transport_command = transport_mechanisms[transport_mech['name']].initiator(*transport_mech['initiator_args'])
	
	#...connect to the transport mechanism that links to the initiator
	pipeline_list.append(transport_command)
	
	#...translate crypto traffic to inbound IPv4 traffic
	pipeline_list.append("python3 inbound_gatekeeper.py")
	
	#Resolve application name...see if it's allowed
	resolved_app_name = resolveAppName(app_name, True)
	
	#...run the executable in a new network namespace
	pipeline_list.append("unshare -n -r ./connect_executable_to_pipe.sh {} {}/24".format(resolved_app_name, this_ipaddr))
	
	#...translate outbound IPv4 traffic to crypto traffic
	pipeline_list.append("python3 outbound_gatekeeper.py > netpipe")
	
	#Save
	pipeline_script_write(pipeline_list, "run_pipeline.sh")
	
	#Return the necessary parameter for the connector to connect to this initiator
	connect_params = {}
	revised_transport_mech = transport_mech.copy()
	if 'initiator_args' in revised_transport_mech:
		del revised_transport_mech['initiator_args']
	
	connect_params['transport_mech'] = revised_transport_mech
	connect_params['tx_symmetric_key'] = rx_symmetric_key
	connect_params['rx_symmetric_key'] = tx_symmetric_key
	connect_params['this_ipaddr'] = remote_ipaddr
	connect_params['remote_ipaddr'] = this_ipaddr
	connect_params['app_name'] = app_name
	connect_params['sc_protectors'] = sc_protectors
	return connect_params


def create_protected_initiator_container_config(transport_mech, remote_peer_id, tx_symmetric_key, rx_symmetric_key, this_ipaddr, remote_ipaddr, app_name, sc_protectors, nacl_nonce):
	connect_params = create_initiator_container_config(transport_mech, remote_peer_id, tx_symmetric_key, rx_symmetric_key, this_ipaddr, remote_ipaddr, app_name, sc_protectors)
	connect_params_jsonbytes = bytes(json.dumps(connect_params), 'ascii')
	
	#Create a NaCl protection box
	f_privkey = open(HOMEDIR + "/.socialsdn/privkey.hex")
	sk = nacl.public.PrivateKey(bytes.fromhex(f_privkey.read().rstrip()))
	f_privkey.close()
	pk = nacl.public.PublicKey(bytes.fromhex(remote_peer_id))
	nacl_box = nacl.public.Box(sk, pk)
	
	#Protect connect_params_jsonbytes
	protected_connect_params_jsonbytes = nacl_box.encrypt(connect_params_jsonbytes, nonce=nacl_nonce)
	
	return protected_connect_params_jsonbytes


def get_verified_connector_container_config(remote_peer_id, protected_config):
	#Create a NaCl protection box
	f_privkey = open(HOMEDIR + "/.socialsdn/privkey.hex")
	sk = nacl.public.PrivateKey(bytes.fromhex(f_privkey.read().rstrip()))
	f_privkey.close()
	pk = nacl.public.PublicKey(bytes.fromhex(remote_peer_id))
	nacl_box = nacl.public.Box(sk, pk)
	
	#Open up connect_params_jsonbytes
	connect_params_jsonbytes = nacl_box.decrypt(bytes.fromhex(protected_config))
	
	return json.loads(connect_params_jsonbytes.decode())
