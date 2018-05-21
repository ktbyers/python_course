#!/usr/bin/env python
"""
1. Read in 'show_arp.xml'

2. Print it to the screen using tostring()

3. Use XPATH to create a dictionary of:

    'ip_addr': {
        'mac_addr': value,
        'intf': value,
    }

        <mac-address>00:62:ec:29:70:fe</mac-address>
        <ip-address>10.220.88.1</ip-address>
        <interface-name>vlan.0</interface-name>

        <mac-address>c8:9c:1d:ea:0e:b6</mac-address>
        <ip-address>10.220.88.20</ip-address>
        <interface-name>vlan.0</interface-name>
"""
from __future__ import unicode_literals, print_function
from lxml import etree
from pprint import pprint

with open('show_arp.xml') as f:
    arp = etree.fromstring(f.read())

print()
print("Print XML Tree out as a string:")
print("-" * 20)
print(etree.tostring(arp, pretty_print=True).decode())

xpath_arp = '//arp-table-entry'
arp_entries = arp.xpath(xpath_arp)

mac_xpath = 'mac-address'
ip_xpath = 'ip-address'
intf_xpath = 'interface-name'

arp_dict = {}
for arp_entry in arp_entries:
    mac_address = arp_entry.xpath(mac_xpath)[0].text
    ip_address = arp_entry.xpath(ip_xpath)[0].text
    intf = arp_entry.xpath(intf_xpath)[0].text
    arp_dict[ip_address] = {
        'mac_addr': mac_address,
        'intf': intf
    }

print()
print("Print out final data structure: ")
print("-" * 20)
pprint(arp_dict)
print()
