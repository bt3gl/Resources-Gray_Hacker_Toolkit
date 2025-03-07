#!/usr/bin/env python

__author__ = "bt3gl"

from scapy.all import *

def save(a):
    wrpcap('packets.pcap', a)

def open():
    p = rdpcap('packets.pcap', p)
    p.show()

def os_finger():
    load_module("p0f")
    p0f(p)

def scan():
    res, unans = sr( IP(dst='192.168.1.114')/TCP(flags='S', dport=(1, 1024)))
    print res.summary()


def sniff_simple():
    p = sniff(iface='wlp1s0', timeout=10, count=5)
    print p.summary()

def sniff_lambda():
    a = sniff(filter='icmp', iface='wlp1s0', timeout=10, count=3,  prn=lambda x:x.summary())
    return a

def tcp_sniff():
    p = sniff(filter="tcp and (port 25 or port 110)")
    p.show()

def sniff_callback():
    def packet_callback(packet):
        print packet.show()

    sniff(filter='icmp', iface='wlp1s0', prn=packet_callback, count=1)


if __name__ == '__main__':
    tcp_sniff()
