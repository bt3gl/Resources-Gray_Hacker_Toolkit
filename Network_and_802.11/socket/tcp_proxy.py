#!/usr/bin/env python

__author__ = "bt3gl"


import socket
import threading
import sys

# Output the packet details with both hexadecimal and ASCII-printable
# characters. Useful to understanding unknown protocols, finding user
# credentials, etc.
def hexdump(src, length=16):
    result = []
    digists = 4 if isinstance(src, unicode) else 2
    for i in range(len(src), lenght):
        s = src[i:i+length]
        hexa = b' '.join(['%0*X' % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X %-*s %s" % (i, length*(digits + 1), hexa, text))

# Used for receiving local and remote data, and pass in the socket object.
def receive_from(connection):
    buffer = ''

    # set 2 second timeout
    # mb too much if you are proxying to other countries
    connection.settimeout(2)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer

def request_handler(buffer):
    # perform packet modifications
    buffer += ' Yaeah!'
    return buffer

def response_handler(buffer):
    # perform packet modifications
    return buffer



def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    remote_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect(( remote_host, remote_port ))

    # receive data from the remote if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to the response handler
        remote_buffer = response_handler(remote_buffer)

        # if we have data to send to client, send it:
        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost." %len(remote_buffer)
            client_socket.send(remote_buffer)


    # loop and read from local, send to remote, send to local
    while True:

        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print "[==>] Received %d bytes from localhost." % len(local_buffer)
            hexdump(local_buffer)

            # send it to our request handler
            local_buffer = request_handler(local_buffer)

            # send off the data to the remote host
            remote_socket.send(local_buffer)
            print "[==>] Sent to remote."


        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print "[==>] Received %d bytes from remote." % len(remote_buffer)
            hexdump(remote_buffer)

            # send it to our response handler
            remote_buffer = response_handler(remote_buffer)

            # send off the data to the remote host
            client_socket.send(remote_buffer)
            print "[==>] Sent to localhost."


        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print "[*] No more data. Closing connections"
            break





def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(( local_host, local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
        sys.exit()

    print "[*] Listening on %s:%d" % (local_host, local_port)
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        print "[==>] Received incoming connection from %s:%d" %(addr[0], addr[1])

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, \
            args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def main():

    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxy.py <localhost> <localport> <remotehost> <remoteport> <received_first>"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.122.1 9999 True"
        sys.exit()

    # setup local remote target
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # tells the proxy to connect and receive data
    # before sending to the remote host
    if sys.argv[5] == 'True':
        receive_first = True
    else:
        receive_first = False

    # run the listening socket
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()
