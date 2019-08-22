#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import easygui

from create_container_config import get_verified_connector_container_config, create_connector_container_config

req_link = easygui.enterbox("Enter the request link:", "SocialSDN")
sender = req_link[0:64]
req = req_link[64:]

try:
	connector_config = get_verified_connector_container_config(sender, req)
	gui_msg = "\n\n"
	gui_msg += "The remote peer {} would like to setup the following connection:\n".format(sender)
	nonce_time = int(req[0:48], 16)
	gui_msg += "\tInitiation Time: {}\n".format(time.strftime("%B %d %Y - %H:%M:%S", time.localtime(nonce_time)))
	gui_msg += "\tApplication: {}\n".format(connector_config['app_name'])
	gui_msg += "\tYour container IP: {}\n".format(connector_config['this_ipaddr'])
	gui_msg += "\tRemote container IP: {}\n".format(connector_config['remote_ipaddr'])
	gui_msg += "\tTransported with: {}\n".format(connector_config['transport_mech'])
	gui_msg += "\n"
	gui_msg += "Do you accept?"
	
	gui_choice = easygui.buttonbox(gui_msg, "SocialSDN", ["Accept", "Modify", "Deny"])
	if gui_choice == "Accept":
		create_connector_container_config(connector_config['transport_mech'], sender, connector_config['tx_symmetric_key'], connector_config['rx_symmetric_key'], connector_config['this_ipaddr'], connector_config['remote_ipaddr'], connector_config['app_name'], connector_config['sc_protectors'])
	
	#TODO: Allow for connection modification
except:
	easygui.msgbox("Failed to create a connection, perhaps the request link is invalid.")
