#!/usr/bin/env python

__author__ = "bt3gl"

from sys import argv, exit
from os import path
from scapy.all import *

def arp_ping(host):
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=host), timeout=2)
    ans.summary(lambda (s, r): r.sprintf("%Ether.src% %ARP.psrc%"))


def icmp_ping(host):
    ans, unans = sr(IP(dst=host)/ICMP())
    ans.summary(lambda (s, r): r.sprintf("%IP.src% is alive"))


def tcp_ping(host, port):
    ans, unans = sr(IP(dst=host)/TCP(dport=port, flags="S"))
    ans.summary(lambda(s, r): r.sprintf("%IP.src% is alive"))

def udp_ping(host, port=0):
    ans, unans = sr(IP(dst=host)/UDP(dport=port))
    ans.summary(lambda(s, r): r.sprintf("%IP.src% is alive"))


if __name__ == '__main__':
    HOST = '192.168.1.25'
    #arp_ping(HOST)
    icmp_ping(HOST)
    #tcp_ping(HOST, 80)
