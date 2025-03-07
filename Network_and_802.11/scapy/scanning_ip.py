#!/usr/bin/env python

__author__ = "bt3gl"

import sys
import random
from scapy.all import IP, TCP, send

def send_syn(dest, src=None, sport=1234, dport=80):
    pkt = IP(dst=dest,src=src)/TCP(sport=sport,dport=dport,flags="S")
    send(pkt)

def scan_ip(dest):
    for i in range(1, 65535):
        send_syn(dest, sport=random.randint(21024, 51024))



if __name__ == '__main__':
    if len(sys.argv) > 1:
        scan_ip(sys.argv[1])
    else:
        print 'Usage: scan_ip <destination>'
