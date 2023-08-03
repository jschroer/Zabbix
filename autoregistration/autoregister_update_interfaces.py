#!/usr/bin/python3
"""
Set host interfaces to defined IP
"""

from pyzabbix import ZabbixAPI
from config import *
import json, sys, time, logging

client_hostname=sys.argv[1]
client_ip=sys.argv[2]

#define logging
stream = logging.StreamHandler(sys.stdout)
log = logging.getLogger('pyzabbix')
log.addHandler(stream)
#log.setLevel(logging.DEBUG)
log.setLevel(logging.ERROR)

# login into Zabbix API
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login(API_USER,API_PASSWORT)

# Disable SSL certificate verification
zapi.session.verify = False

# Specify a timeout (in seconds)
zapi.timeout = 5.1

#search the host we will modify
host = zapi.host.get(filter={'host':client_hostname},selectInterfaces="extend",limit=4)

# get the hostID into separate variable
hostIdValue = host[0]['hostid']

# loop over interfaces and update ip or delete them
for interface in host[0]['interfaces']:
    if interface['main'] == "1":     # if it is a default interface than change ip
      interface['ip'] = client_ip
      zapi.hostinterface.update(interface);
    else:
      zapi.hostinterface.delete(interface['interfaceid']) # if it is a additional interface delete it

