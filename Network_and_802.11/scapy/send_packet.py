#!/usr/bin/env python

__author__ = "bt3gl"

from scapy.all import *

packet = IP(dst="192.168.1.114")/ICMP()/"Helloooo!"
#send(packet, loop=1)
send(packet)
packet.show()
