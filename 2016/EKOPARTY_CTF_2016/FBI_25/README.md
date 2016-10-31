#EKOPARTY CTF 2016: FBI 25

###Welcome to the dark side
```
At Silk Road, every precaution is made to ensure your anonymity and security, from connecting to the site, to making your transactions, to receiving your items.

https://silkroadzpvwzxxv.onion
```

##Solution
I wasn't really know what to do at first because i can't get into the site for some reason.
After some research I finally know about onion url.
>Wikipedia: .onion is a special-use top level domain suffix designating an anonymous hidden service reachable via the Tor network. 

So, I download Tor Browser and I am able to get into the site.
I checked the source code and get the flag.

```
<!-- 25 - EKO{buy_me_some_b0ts} -->
<html>
  <head>
    <meta http-equiv="Content-type" content="text/html; charset=UTF-8" />
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <title>
      Silk Road
    </title>
	...
```

Flag:
>EKO{buy_me_some_b0ts}
