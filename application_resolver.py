#!/usr/bin/env python3
# -*- coding: utf-8 -*-

ALLOWED_APPNAMES = ["linphone"]

def resolveAppName(app_name):
	if app_name in ALLOWED_APPNAMES:
		return app_name
	else:
		raise Exception("Application unknown or not allowed.")
