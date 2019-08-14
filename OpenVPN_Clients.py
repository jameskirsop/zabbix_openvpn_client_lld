#!/usr/bin/env python3
conf_dir = '/etc/openvpn/nms/client-configs'

import telnetlib
import re
from os import listdir
import json
import csv
import time

returnList = []
listConfigs = listdir(conf_dir)

con = telnetlib.Telnet('localhost',7505)
con.read_until(b"info\r\n",2)
time.sleep(.1)
con.write(b"status 2\n")
con.expect([re.compile(b",\d{10,}\\r\\n",)])
con.expect([b'HEADER,'])
first = con.read_until(b'HEADER,')
for row in csv.DictReader(first.decode('ascii').rstrip('\r\nHEADER,').split("\r\n")):
    returnList.append({
        "{#HOSTNAME}" : row['Common Name'],
        "{#VPNv4Address}" : row['Virtual Address'],
        "{#VPNv6Address}" : row['Virtual IPv6 Address'],
        "{#PUBLICADDRESS}" : row['Real Address']
    })
    listConfigs.remove(row['Common Name'])
for config in listConfigs:
    returnList.append({
        "{#HOSTNAME}" : config,
        "{#VPNv4Address}" : None,
        "{#VPNv6Address}" : None,
        "{#PUBLICADDRESS}" : None,
    })
con.write(b"exit\n")
res = con.read_all()
con.close()
print(json.dumps({"data":returnList},indent=4))