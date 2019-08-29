#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import easygui

easygui.buttonbox("Network pipeline is running.", "SocialSDN", ["STOP"])
os.kill(-1, signal.SIGTERM)
