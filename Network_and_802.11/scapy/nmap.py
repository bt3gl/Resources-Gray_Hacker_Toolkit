#!/usr/bin/env python

__author__ = "bt3gl"

from scapy.all import *
import random

HOST = "192.168.1.25"
PORTS = [22, 23, 25, 80, 443, 8000]

def nmap():
    for dport in PORTS:

        sport = random.randint(1025, 65534)
        resp = sr1(IP(dst=HOST)/TCP(sport=sport,dport=dport,flags="S"), timeout=1,verbose=0)

        if (str(type(resp)) == "<type 'NoneType'>"):
            print HOST + ":" + str(dport) + " is filtered (dropped)."

        elif(resp.haslayer(TCP)):
            if(resp.getlayer(TCP).flags == 0x12):
                send_rst = sr(IP(dst=HOST)/TCP(sport=sport,dport=dport,flags="R"),timeout=1,verbose=0)
                print HOST + ":" + str(dport) + " is open."
            elif (resp.getlayer(TCP).flags == 0x14):
                print HOST + ":" + str(dport) + " is closed."

        elif(resp.haslayer(ICMP)):
            if(int(resp.getlayer(ICMP).type)==3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                print HOST + ":" + str(dport) + " is filtered (dropped)."

if __name__ == '__main__':
    nmap()
