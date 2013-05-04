#coding:utf8

import urllib
import json
import sys

def req(r):
    print r
    q = urllib.urlopen(r)
    s = q.read()
    try:
        l = json.loads(s)
        print l
    except:
        print "error\n"
        sys.stderr.write(r+'\n'+s+'\n')
    return l

BASE = 'http://localhost:5000/'

r = BASE+'findAMatch?uid=0&score=50&scoreOff=20'
req(r)

r = BASE+'findAMatch?uid=0&score=1000&scoreOff=50'
req(r)
