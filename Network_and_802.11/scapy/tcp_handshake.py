#!/usr/bin/env python

__author__ = "bt3gl"

from scapy.all import *


ip = IP(src='192.168.1.114', dst='192.168.1.25')
SYN = TCP(sport=1024, dport=80, flags='S', seq=12345)
packet = ip/SYN
SYNACK = sr1(packet)
ack = SYNACK.seq + 1
ACK = TCP(sport=1024, dport=80, flags='A', seq=12346, ack=ack)
send(ip/ACK)
PUSH = TCP(sport=1024, dport=80, flags='', seq=12346, ack=ack)
data = "HELLO!"
send(ip/PUSH/data)
