#!/usr/bin/env python
from __future__ import print_function, unicode_literals

from jnpr.junos import Device
from lxml import etree
from getpass import getpass

juniper_srx = {
    "host": "srx1.twb-tech.com",
    "user": "pyclass",
    "password": getpass(),
}

a_device = Device(**juniper_srx)
a_device.open()

# show version | display xml rpc
# get-software-information
# show_version = a_device.rpc.get_software_information()

# get-lldp-neighbors-information
lldp = a_device.rpc.get_lldp_neighbors_information()
print(etree.tostring(lldp, encoding='unicode', pretty_print=True))
