#!/bin/bash

CONTAINER=$1

HOST_DEV=tun$CONTAINER
GUEST_DEV=eth1

#Start a socat bi-directional relay
cat /dev/stdin | socat -d -d STDIO TUN,tun-name=$HOST_DEV > /dev/stdout &

#Wait for the socat relay to start
#TODO: This is a hack for testing purposes, actually check for creation of HOST_DEV device
sleep 5

mkdir -p /var/run/netns
PID=$(docker inspect -f '{{.State.Pid}}' $CONTAINER)
ln -s /proc/$PID/ns/net /var/run/netns/$PID
ip link set $HOST_DEV netns $PID name $GUEST_DEV
ip netns exec $PID ip addr add 192.168.1.1/24 dev $GUEST_DEV
ip netns exec $PID ip link set $GUEST_DEV up
rm -r /var/run/netns/$PID

#TODO: Change this to waiting for a CTRL+C interrupt
while true
do
	sleep 1
done
