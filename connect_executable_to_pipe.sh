#!/bin/bash

MY_EXEC=$1
IP_ADDR=$2

$MY_EXEC > /dev/null &
EXEC_PID=$!
socat -d -d STDIO TUN:$IP_ADDR,tun-name=eth0,up

#When socat is killed also kill EXEC_PID
kill $EXEC_PID
