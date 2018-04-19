#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import jinja2

intf_config = """
interface FastEthernet4
 description *** LAN connection (don't change) ***
 ip address {{ ip_addr }} {{ netmask }}
 duplex auto
 speed auto

"""

intf_vars = {
    'ip_addr': '10.220.88.20',
    'netmask': '255.255.255.0',
}

template = jinja2.Template(intf_config)
output = template.render(**intf_vars)
print(output)
