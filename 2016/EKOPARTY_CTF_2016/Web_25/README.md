#EKOPARTY CTF 2016: Web 25

###Mr. Robot
```
Disallow it!
```

##Solution
Robot? Disallow? Easy!
Let's search for robots.txt
>https://ctf.ekoparty.org/robots.txt

```
User-agent: *
Disallow: /static/wIMti7Z27b.txt
```
So, just proceed to
>https://ctf.ekoparty.org/static/wIMti7Z27b.txt

```
EKO{robot_is_following_us}
```

Flag:
>EKO{robot_is_following_us}
