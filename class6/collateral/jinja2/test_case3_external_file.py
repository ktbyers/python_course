#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import jinja2

with open("intf_config.j2") as f:
    intf_config = f.read()

intf_vars = {
    'ip_addr': '10.220.88.20',
    'netmask': '255.255.255.0',
}

template = jinja2.Template(intf_config)
output = template.render(**intf_vars)
print(output)
