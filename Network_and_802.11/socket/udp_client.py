#!/usr/bin/env python

__author__ = "bt3gl"


import socket

# Defining constants
HOST = '127.0.0.1'
PORT = 9000
DATA = 'AAABBBCCC'


def udp_client():

    # Create a socket object
    # AF_INET parameter: to use standard IPv4 address
    # SOCK_DGRAM: to indicate udp client
    client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)

    # Send data
    client.sendto(DATA, ( HOST, PORT ))

    # Receive some data
    data, addr = client.recvfrom(4096)
    print data, addr



if __name__ == '__main__':
    udp_client()
