#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ALLOWED_APPNAMES = ["linphone", "./protected_linphone.sh"]

def resolveAppName(app_name, isInitiator):
	if app_name == "TIMESYNC":
		if isInitiator:
			return "./act_timeserver.sh"
		else:
			return "./act_timeclient.sh"
	
	if app_name == "Droopy-to-Firefox":
		if isInitiator:
			return "/opt/socialsdn/droopy_socialsdn_server.sh"
		else:
			return "/opt/socialsdn/firefox_socialsdn_client.sh"
	
	if app_name == "UNIXsocket-to-Firefox":
		if isInitiator:
			return "gui_tcp_to_unix.sh"
		else:
			return "/opt/socialsdn/firefox_socialsdn_client.sh"
	
	if app_name in ALLOWED_APPNAMES:
		return app_name
	else:
		raise Exception("Application unknown or not allowed.")
