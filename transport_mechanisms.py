#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests

from scapy.all import IP

def invalidHostname(host):
	for c in host:
		if c not in "abcdefghijklmnopqrstuvwxyz01234567890.":
			return True
	return False

def getOutboundSourceIP(dst_ip):
	pkt = IP(dst=dst_ip)
	return pkt.src

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

class Ngrok:
	def getInitiatorArgs():
		return [("Ngrok API Base URL", str), ("TCP Listen Port", int), ("Ngrok Tunnel Name", str)]
	
	def resolveInitiatorArgs(args):
		ret_args = []
		ret_args.append(args[1])
		return ret_args
	
	def resolveConnectorArgs(args):
		ngrok_api_baseurl = args[0]
		tcp_listen_port = args[1]
		ngrok_tunnel_name = args[2]
		
		#Get the IP address on this machine that routes to ngrok_api_baseurl
		this_client_ip = getOutboundSourceIP(ngrok_api_baseurl)
		
		#Open a new ngrok tunnel to `TCP Listen Port`
		open_req = requests.post("http://" + ngrok_api_baseurl + ":4040/api/tunnels", json={"addr": "{}:{}".format(this_client_ip, tcp_listen_port), "proto": "tcp", "name": ngrok_tunnel_name})
		
		#Delete request would be: requests.delete("http://" + ngrok_api_baseurl + "/api/tunnels/" + ngrok_tunnel_name)
		
		if open_req.status_code != 201:
			raise Exception("Could not open the Ngrok tunnel")
		
		public_url = str(json.loads(open_req.text)['public_url'])
		
		#Remove the tcp:// part
		public_url = public_url[6:]
		
		#Split into the hostname and port number parts
		public_url = public_url.split(":")
		ngrok_hostname = public_url[0]
		
		if invalidHostname(ngrok_hostname):
			raise Exception("Ngrok generated an invalid hostname")
		
		ngrok_portnumber = int(public_url[1])
		if ngrok_portnumber < 0 or ngrok_portnumber > 65535:
			raise Exception("Ngrok generated an invalid TCP port number")
		
		return [ngrok_hostname, ngrok_portnumber]
	
	
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
transport_mechanisms['ngrok'] = Ngrok
