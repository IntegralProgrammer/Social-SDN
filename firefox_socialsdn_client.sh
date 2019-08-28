#!/bin/bash
unshare -u -m -r /bin/bash -c '(mount -t tmpfs tmpfs ~/.mozilla) && firefox -no-remote'
