#!/usr/bin/env python3
conf_dir = ''

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
    # print(row)
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

# print('========')
# print(res.decode('ascii'))
# print(listConfigs)

# re.search(b",\d{10,}\\r\\n",b"08:29:45 2019,1565735385\r\n")

# re.search("[A-z]","aaa")
# con = telnetlib.Telnet('localhost',7505)
# con.read_lazy()
# time.sleep(.1)
# con.write(b"status 2\n")
# con.write(b"exit\n")
# res = con.read_all()
# print(res)
# print(listdir(conf_dir))
# print(len(listdir(conf_dir)))

# tnc = telnetlib.Telnet
# conn = telnetlib.Telnet('localhost',7505)
# conn.set_debuglevel(1)
# conn.read_lazy()
# conn.write(b"status 2\n")
# conn.write(b"exit\n\n")
# print(conn.read_until(b'END\r\n',timeout=2).decode('ascii'))
# conn.close()

# conn.read_until(b"INFO:",timeout=2)
# conn.open()
# conn.read_until(b">INFO:OpenVPN Management Interface Version 1 -- type 'help' for more info")

#con.read_until("'help' for more info")
# con.read_lazy()