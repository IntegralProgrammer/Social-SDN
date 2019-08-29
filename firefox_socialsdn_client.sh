#!/bin/bash
exec unshare -u -m -r /bin/bash -c '(mount -t tmpfs tmpfs ~/.mozilla) && exec firefox -no-remote'
