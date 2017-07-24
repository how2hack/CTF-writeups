#!/usr/bin/env python

import requests
import hashlib
import string
import itertools

def sha1(content):
    Hash = hashlib.sha1()
    Hash.update(content)
    return Hash.digest()

url = 'https://quiz.ais3.org:32670/'

pdf1 = open("shattered-1.pdf").read()[:330]
pdf2 = open("shattered-2.pdf").read()[:330]

if sha1(pdf1) == sha1(pdf2):
	print 'FOUND'
	headers = {'User-Agent' : 'Mozilla/5.0'}
	values = {'username' : pdf1, 'password' : pdf2}
	session = requests.Session()
	print session.post(url, headers=headers, data=values).text.encode("utf-8")
