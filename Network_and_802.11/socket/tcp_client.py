#!/usr/bin/env python

__author__ = "bt3gl"


import socket

# Defining constants
HOST = 'localhost'
PORT = 9090
DATA = 'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n'


def tcp_client():

    # Create a socket object
    # AF_INET parameter: to use standard IPv4 address
    # SOCK_STREAM: to indicate tcp client
    client = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

    # Connect the client
    client.connect(( HOST, PORT ))

    # Send data
    client.send(DATA)

    # Receive some data
    response = client.recv(4096)
    print response



if __name__ == '__main__':
    tcp_client()
