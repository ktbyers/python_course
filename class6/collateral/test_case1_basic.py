#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import jinja2

intf_config = """
interface FastEthernet4
 description *** LAN connection (don't change) ***
 ip address 10.220.88.20 255.255.255.0
 duplex auto
 speed auto

"""

template = jinja2.Template(intf_config)
output = template.render()
print(output)
