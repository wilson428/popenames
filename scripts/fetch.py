
import re
import json
from lxml.html import etree, fromstring
from utils import download, write

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
    data["end"] = re.findall("(\d+)\)", pope.xpath("text()")[0])[0]            
    moniker = re.findall("^(Blessed|[A-z]+\. )*(.*?)([IXV]*)$", data["fullname"])[0]
    data["title"],data["name"],data["number"] = [x.strip() for x in moniker]

    #456-75 -> 456-475
    if len(data["end"]) == 2:            
        data["end"] = data["start"][:-2] + data["end"]
    popes.append(data)        
write(json.dumps(popes, indent=2), "popes.json")
print "found data for %i popes" % len(popes)
