#EKOPARTY CTF 2016: Forensics 75

###Damaged
```
All you have to do is to see this damaged image!

Attachment
for75_165560e4a08b23f7.zip
```

##Solution
Given a bitmap image file, the header of the file is removed, let's fix it!

>https://en.wikipedia.org/wiki/BMP_file_format

According to the given link, adding the hex text below to the beginning of the file will fix the image.

```
42 4D 36 75 00 00 00 00 00 00 36 00 00 00
```

open it and :D

![bump](flag.bmp)

Flag:
>EKO{b1tm4p_r3c}
