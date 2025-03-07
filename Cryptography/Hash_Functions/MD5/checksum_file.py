#!/usr/bin/env python

__author__ = "bt3gl"

'''
Calculate the MD5 checksum of a file.
We work on chunks to avoid using too much memory when the file is large.
'''

import os
from Crypto.Hash import MD5
def get_file_checksum(filename):
    h = MD5.new()
    chunk_size = 8192
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                break
            h.update(chunk)
    return h.hexdigest()
