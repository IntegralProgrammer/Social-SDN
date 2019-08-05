#!/bin/bash

mkdir -p /opt/socialsdn/

echo "Copying necessary files..."

cp -v ../connect_executable_to_pipe.sh /opt/socialsdn/
chmod +x /opt/socialsdn/connect_executable_to_pipe.sh

cp -v ../inbound_gatekeeper.py /opt/socialsdn/
cp -v ../outbound_gatekeeper.py /opt/socialsdn/
cp -v ../debugger_passthrough.py /opt/socialsdn/
cp -v ../create_container_config.py /opt/socialsdn/
cp -v ../transport_mechanisms.py /opt/socialsdn/
cp -v ../application_resolver.py /opt/socialsdn/

cp -v ../initialize_socialsdn_directory.sh /usr/bin/
chmod +x /usr/bin/initialize_socialsdn_directory.sh

echo "...done."
