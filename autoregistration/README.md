# autoregistration

## tools for autoregistration in zabbix

This tools can be used during autoregistration to solve some standart problems I run into.

## autoregister_add_snmptemplate.py
This tool can be used to add SNMP Templates on autoregistration. Because normally no SNMP device is created during autoregister it add a standart SNMP device equal to the settings of the standart agent-device as first.

Register in scripts section of zabbix with <path>/autoregister_add_snmptemplate.py {HOST.HOST} "SNMP template"

## autoregister_update_interfaces.py
