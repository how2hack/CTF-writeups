#EKOPARTY CTF 2016: Web 50

###RFC 7230
```
Get just basic information from this server (ctf.ekoparty.org).
```

##Solution
>curl -I ctf.ekoparty.org

```
HTTP/1.1 301 Moved Permanently
Server: EKO{this_is_my_great_server}
Date: Fri, 28 Oct 2016 15:06:06 GMT
Content-Type: text/html
Content-Length: 178
Connection: keep-alive
Location: https://ctf.ekoparty.org/
```

There it is!

Flag:
>EKO{this_is_my_great_server}
