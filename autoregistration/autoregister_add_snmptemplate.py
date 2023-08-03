#!/usr/bin/python3
"""
Add a SNMP template to a existing host, if no SNMP interface exist it will create one
"""

from pyzabbix import ZabbixAPI
from config import *
import json, sys, time, logging

client_hostname=sys.argv[1]
template=sys.argv[2]

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
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


#search the template we should add
templ = zapi.template.get(filter={'host':template},limit=4 )

# is the template found?
if len(templ) < 1:
   # template doesn't exists, we can stop here
   exit()
else:
   templateIdValue = templ[0]['templateid']

# just a flag to see if there is already a snmp interface, filed in the following loop

have_snmp_interface = 0
# loop over interfaces and search for an SNMP interface
for interface in host[0]['interfaces']:
    if interface['main'] == "1" and interface['type'] == "2":
      have_snmp_interface =1


# if there exist no snmp interface than let create one
if have_snmp_interface == 0:
  # loop over interfaces and search for the standart agent interface as template
  for interface in host[0]['interfaces']:
     if interface['main'] == "1" and interface['type'] == "1":
       # found, lets create a SNMP Interface
       new_interface= {}
       new_interface['main']   = "1"
       new_interface['hostid'] = hostIdValue
       new_interface['type']   = "2"
       new_interface['useip']  = interface['useip']
       new_interface['ip']     = interface['ip']
       new_interface['dns']    = interface['dns']
       new_interface['port']   = "161"
#       new_interface['port']   = "3401"


       new_interface['details']={}
       new_interface['details']['version'] = "2"
       new_interface['details']['bulk'] = "1"
       new_interface['details']['community'] = "{$SNMP_COMMUNITY}"
       zapi.hostinterface.create(new_interface)


# add the template
#zapi.templates.massadd(templates={"templateid":templateIdValue},hosts={"hostid": hostIdValue});
zapi.host.massadd(templates={"templateid":templateIdValue},hosts={"hostid": hostIdValue});

