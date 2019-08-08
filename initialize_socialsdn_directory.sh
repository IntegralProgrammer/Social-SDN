#!/bin/bash

# This file should be installed under /usr/bin/

echo "Copying necessary files..."
cp -v /opt/socialsdn/connect_executable_to_pipe.sh . || exit;
cp -v /opt/socialsdn/inbound_gatekeeper.py . || exit;
cp -v /opt/socialsdn/outbound_gatekeeper.py . || exit;
cp -v /opt/socialsdn/debugger_passthrough.py . || exit;
cp -v /opt/socialsdn/create_container_config.py . || exit;
cp -v /opt/socialsdn/transport_mechanisms.py . || exit;
cp -v /opt/socialsdn/application_resolver.py . || exit;
cp -v /opt/socialsdn/inbound_sidechannel_passthrough.py inbound_sidechannel_shaper.py || exit;
cp -v /opt/socialsdn/outbound_sidechannel_passthrough.py outbound_sidechannel_shaper.py || exit;
echo "...done."

echo "Creating the named pipe..."
mkfifo netpipe
echo "...done."

echo "Sucessfully initialized this directory for use with SocialSDN."
