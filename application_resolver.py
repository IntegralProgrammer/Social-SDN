#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ALLOWED_APPNAMES = ["linphone", "./protected_linphone.sh"]

def resolveAppName(app_name, isInitiator):
	if app_name == "TIMESYNC":
		if isInitiator:
			return "./act_timeserver.sh"
		else:
			return "./act_timeclient.sh"
	
	if app_name in ALLOWED_APPNAMES:
		return app_name
	else:
		raise Exception("Application unknown or not allowed.")
