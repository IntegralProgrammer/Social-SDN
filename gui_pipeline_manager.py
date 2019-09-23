#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import easygui

easygui.buttonbox("Network pipeline is running.", "SocialSDN", ["STOP"])

#Prevent starting again using the same keypads
os.remove('tx_keymappings.json')
os.remove('rx_keymappings.json')
os.remove('inner_run_pipeline.sh')

#Stop everything
os.kill(-1, signal.SIGTERM)
