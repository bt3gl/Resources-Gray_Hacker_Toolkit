#!/usr/bin/env python

__author__ = "bt3gl"


'''
EXAMPLE FROM ASIS 2013, WITH THE CONCATENATED HASH:

7e1321b3c8423b30c1cb077a2e3ac4f0a2a551a6458a8de22446cc76d639a9e98fc42c6cddf9966db3b09e843650343578b04d5e377d298e78455efc5ca404d5f4c9385f1902f7334b00b9b4ecd164de8bf8854bebe108183caeb845c7676ae48fc42c6ddf9966db3b09e84365034357327a6c4304ad5938eaf0efb6cc3e53dc7ff9ea9a069bd793691c422fb818c07b

'''

import md5


# the entire flag

m1 = '7e1321b3c8423b30c1cb077a2e3ac4f0'
m2 = 'a2a551a6458a8de22446cc76d639a9e9'
m3 = '8fc42c6ddf9966db3b09e84365034357'
m4 = '8b04d5e3775d298e78455efc5ca404d5'
m5 = 'f4c9385f1902f7334b00b9b4ecd164de'
m6 = '8bf8854bebe108183caeb845c7676ae4'
m7 = '8fc42c6ddf9966db3b09e84365034357'
m8 = '327a6c4304ad5938eaf0efb6cc3e53dc'
m9 = '7ff9ea9a069bd793691c422fb818c07b'

all = [m1, m2, m3, m4, m5, m6, m7, m8, m9]

for m in all:
    a = md5.md5(m)
    print "md5 object", a
    print "digest(): ", a.digest()
    print "hexdigest(): ", a.hexdigest()
    print





# last part

for a in "abcdef0123456789":
    for b in "abcdef0123456789":
        if "7ff9ea9a069bd793691c422fb818c07b" == md5.md5('ASIS_' + a + b).hexdigest():
            print 'ASIS_' + a + b
