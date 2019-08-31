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
cp -v ../inbound_sidechannel_passthrough.py /opt/socialsdn/
cp -v ../outbound_sidechannel_passthrough.py /opt/socialsdn/
cp -v ../timeserver.py /opt/socialsdn/
cp -v ../timeclient.py /opt/socialsdn/
cp -v ../gui_create_initiator.py /opt/socialsdn/
cp -v ../gui_create_connector.py /opt/socialsdn/
cp -v ../gui_pipeline_manager.py /opt/socialsdn/
cp -v ../add_contact.py /opt/socialsdn/

cp -v ../run_pipeline.sh /opt/socialsdn/
chmod 555 /opt/socialsdn/run_pipeline.sh

cp -v ../firefox_socialsdn_client.sh /opt/socialsdn/
chmod +x /opt/socialsdn/firefox_socialsdn_client.sh

cp -v ../droopy_socialsdn_server.sh /opt/socialsdn/
chmod +x /opt/socialsdn/droopy_socialsdn_server.sh

cp -v ../gui_tcp_to_unix.sh /usr/bin/
chmod +x /usr/bin/gui_tcp_to_unix.sh

cp -v ../gui_unix_to_tcp.sh /usr/bin/
chmod +x /usr/bin/gui_unix_to_tcp.sh

mkdir /opt/socialsdn/trafficshaping
mkdir /opt/socialsdn/trafficshaping/inbound
mkdir /opt/socialsdn/trafficshaping/outbound
mkdir /opt/socialsdn/trafficshaping/desc
mkdir /opt/socialsdn/trafficshaping/names

echo "Installing traffic shaping policies"
SUM=$(cat ../TrafficShapingDescriptions/voip_model.txt ../inbound_sidechannel_voipmodel.py ../outbound_sidechannel_voipmodel.py | sha256sum - | cut -d ' ' -f1)
cp -v ../inbound_sidechannel_voipmodel.py /opt/socialsdn/trafficshaping/inbound/$SUM.py
cp -v ../outbound_sidechannel_voipmodel.py /opt/socialsdn/trafficshaping/outbound/$SUM.py
cp -v ../TrafficShapingDescriptions/voip_model.txt /opt/socialsdn/trafficshaping/desc/$SUM.txt
echo -ne "VoIP Model" > /opt/socialsdn/trafficshaping/names/$SUM.txt


cp -v ../act_timeserver.sh /opt/socialsdn/
chmod +x /opt/socialsdn/act_timeserver.sh

cp -v ../act_timeclient.sh /opt/socialsdn/
chmod +x /opt/socialsdn/act_timeclient.sh

cp -v create_identity_keypair.py /opt/socialsdn/

cp -v ../initialize_socialsdn_directory.sh /usr/bin/
chmod +x /usr/bin/initialize_socialsdn_directory.sh

cp -v setup_socialsdn_identity.sh /usr/bin/
chmod +x /usr/bin/setup_socialsdn_identity.sh

echo "...done."
