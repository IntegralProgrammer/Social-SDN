#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from create_container_config import get_verified_connector_container_config, create_connector_container_config

#req = input("Enter the request:")
#sender = input("Enter the sender's id:")

req_link = input("Enter the request link: ")
sender = req_link[0:64]
req = req_link[64:]

try:
	connector_config = get_verified_connector_container_config(sender, req)
	print("")
	print("")
	print("The remote peer {} would like to setup the following connection:".format(sender))
	nonce_time = int(req[0:48], 16)
	print("\tInitiation Time: {}".format(time.localtime(nonce_time)))
	print("\tApplication: {}".format(connector_config['app_name']))
	print("\tYour container IP: {}".format(connector_config['this_ipaddr']))
	print("\tRemote container IP: {}".format(connector_config['remote_ipaddr']))
	print("\tTransported with: {}".format(connector_config['transport_mech']))
	print("")
	if (input("Do you accept? [y/N]") == 'y'):
		print("Accepting the connection.")
		create_connector_container_config(connector_config['transport_mech'], sender, connector_config['tx_symmetric_key'], connector_config['rx_symmetric_key'], connector_config['this_ipaddr'], connector_config['remote_ipaddr'], connector_config['app_name'], connector_config['sc_protectors'])
	else:
		print("Denying the connection.")
	
except:
	print("Invalid message!")
