#!/usr/bin/env python
"""
Use Netmiko and TextFSM to retrieve 'show ip int brief' from pynet-rtr2 as structured
data.

This will require that you install ntc-templates into the lab environment as follows:

# cd to the base of your home directory
$ cd ~

# Git clone ntc-templates into this directory
$ git clone https://github.com/networktocode/ntc-templates

# At the end of this you should have ntc-templates on this path
$ ls ~/ntc-templates/templates/index

In order to do this, besides adding ntc-templates into the above path, you will also
need to add the 'use_textfsm=True' argument when calling the send_command() method.

Note, if your TextFSM lookup fails, you will probably get unstructured data returned to
you. You can also set this environment variable (if your TextFSM lookup is failing).

export NET_TEXTFSM=/path/to/ntc-templates/templates/

After you have retrieved this 'show ip int brief' output as structured data. Parse the
returned data structure and print out the IP address associated with FastEthernet4.
"""

from __future__ import print_function, unicode_literals
from getpass import getpass
from netmiko import ConnectHandler

password = getpass()

pynet_rtr2 = {
    'device_type': 'cisco_ios',
    'host': 'cisco2.twb-tech.com',
    'username': 'pyclass',
    'password': password,
}

net_connect = ConnectHandler(**pynet_rtr2)
show_ip = net_connect.send_command('show ip int brief', use_textfsm=True)

print()
print(">>>>>")
for intf_dict in show_ip:
    if intf_dict['intf'] == 'FastEthernet4':
        print("IP address of FA4: {ipaddr}".format(**intf_dict))
print(">>>>>")
print()
