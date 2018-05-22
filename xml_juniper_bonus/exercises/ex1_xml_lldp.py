#!/usr/bin/env python
"""
Read in the file named 'show_lldp.xml'. This file is from
'show lldp neighbors | display xml' on a Juniper SRX (modified somewhat).

Use etree.tostring() to print out the XML tree as a string.

Use getchildren() or list indices to find the one child element of the root element. Print out
this element's tag name.

Using either a for-loop or getchildren(), find the text values associated with the following
tags: 'lldp-local-interface', 'lldp-remote-system-name', 'lldp-remote-port-description'. Save
these three items to a data structure with the following format:

{ local_intf:
    {
        'remote_port': value,
        'remote_sys_name': value,
    }
}

Print this data structure out to the screen. Your printed data structure should match the
following:

{'fe-0/0/7.0': {'remote_port': '24', 'remote_sys_name': 'twb-sf-hpsw1'}}

"""
from __future__ import unicode_literals, print_function
from lxml import etree
from pprint import pprint

with open('show_lldp.xml') as f:
    lldp = etree.fromstring(f.read())

print()
print("Print XML Tree out as a string:")
print("-" * 20)
print(etree.tostring(lldp, pretty_print=True).decode())

print('\n\n')
print("Print one child element of the root element:")
print("-" * 20)
lldp_child = lldp.getchildren()[0]
print(lldp_child.tag)

for child in lldp_child:
    if child.tag == 'lldp-local-interface':
        local_intf = child.text
    elif child.tag == 'lldp-remote-system-name':
        remote_sys_name = child.text
    elif child.tag == 'lldp-remote-port-description':
        remote_port = child.text

lldp_dict = {
    local_intf: {
        'remote_sys_name': remote_sys_name,
        'remote_port': remote_port,
    }
}

print('\n\n')
print("Parse the returned data and create a dictionary.")
print("-" * 20)
pprint(lldp_dict)
print('\n\n')
