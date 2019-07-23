#!/bin/bash

cp ../SocatAdapter3.py container_side/
cp ../SocatAdapter3.py host_side/

cp ../inbound_gatekeeper.py container_side/
cp ../inbound_gatekeeper.py host_side/

cp ../outbound_gatekeeper.py container_side/
cp ../outbound_gatekeeper.py host_side/

cp ../connect_container_to_pipe.sh .
chmod u+x connect_container_to_pipe.sh

mkfifo netpipe
