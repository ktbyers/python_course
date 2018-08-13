#!/usr/bin/env python
"""
Read in the file named 'show_arp.xml'. This file is from 'show arp | display xml' on a
Juniper SRX (modified somewhat).

Use etree.tostring() to print out the XML tree as a string.

Use XPath parsing to find all of the arp entries and to construct the following
dictionary:

{
  '10.220.88.1':
    {
        'intf': 'vlan.0',
        'mac_addr': '00:62:ec:29:70:fe'
    },
  '10.220.88.20':
    {
        'intf': 'vlan.0',
        'mac_addr': 'c8:9c:1d:ea:0e:b6'
    }
}

Print this dictionary out to standard output.
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
