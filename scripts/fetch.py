#!/usr/bin/env python

import re
import json
from lxml.html import etree, fromstring
from utils import download, write

def roman2arabic(value):
    if not value:
        return None
        
    total = 0
    values = { 'I': 1, 'V': 5, 'X': 10 }
    
    prevValue = 0
    for char in value:
        if values[char] > prevValue:
            total -= prevValue
        else:
            total += prevValue
        prevValue = values[char]
    total += prevValue
    
    return total
    
roster = fromstring(download("http://www.newadvent.org/cathen/12272b.htm")).xpath("//ol/li")
popes = []

for pope in roster:
    if len(pope.xpath("a")):
        data = {
            "fullname": pope.xpath("a/text()")[0],
            "url": "http://www.newadvent.org/" + pope.xpath("a/@href")[0][3:]
        }
        #bio = fromstring(download(data["url"]))
        
    else:
        data = {
            "fullname": pope.xpath("text()")[0].strip().split(" (")[0],
            "url": None
        }
    data["start"] = re.findall("\((\d+)", pope.xpath("text()")[0])[0]
    try:
        data["end"] = re.findall("(\d+)\)", pope.xpath("text()")[0])[0]
    except IndexError, e:
        data["end"] = None
    data["nicknames"] = re.findall(" \((.*?)\)", data["fullname"])
    moniker = re.findall("^(Blessed|[A-z]+\. )*(.*?)([IXV]*)$", re.sub(" \((.*?)\)", "", data["fullname"]))[0]
    data["title"],data["name"],data["number"] = [x.strip() for x in moniker]
    data["decimal"] = roman2arabic(data["number"])

    #456-75 -> 456-475
    if data["end"] and len(data["end"]) == 2:            
        data["end"] = data["start"][:-2] + data["end"]
    data["start"] = int(data["start"])
    data["end"] = None if not data["end"] else int(data["end"])
    
    popes.append(data)        
write(json.dumps(popes, indent=2), "popes.json")
print "found data for %i popes" % len(popes)
