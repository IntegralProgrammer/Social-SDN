#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def invalidHostname(host):
	for c in host:
		if c not in "abcdefghijklmnopqrstuvwxyz01234567890.":
			return True
	return False

class Netcat:
	def getInitiatorArgs():
		return [("Hostname", str), ("TCP Port", int)]
	
	def resolveInitiatorArgs(args):
		ret_args = []
		ret_args.append(args[1])
		return ret_args
	
	def resolveConnectorArgs(args):
		ret_args = []
		ret_args.append(args[0])
		ret_args.append(args[1])
		return ret_args
	
	def initiator(tcp_port):
		if type(tcp_port) != int:
			raise Exception("Wrong data type for initiator TCP port.")
		
		if tcp_port not in range(1024, 65536):
			raise Exception("Invalid port number")
		
		return "nc -l -p {} -q 0".format(tcp_port)
	
	def connector(host, tcp_port):
		if type(host) != str:
			raise Exception("Wrong data type for connector host.")
		
		if invalidHostname(host):
			raise Exception("Invalid connector hostname.")
		
		if type(tcp_port) != int:
			raise Exception("Wrong data type for connector TCP port.")
		
		if tcp_port not in range(1024, 65536):
			raise Exception("Invalid port number")
		
		return "nc {} {} -q 0".format(host, tcp_port)

transport_mechanisms = {}
transport_mechanisms['netcat'] = Netcat
