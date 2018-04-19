#!/usr/bin/env python
from __future__ import unicode_literals, print_function
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader('.')

intf_vars = {
    'ip_addr': '10.220.88.20',
    'netmask': '255.255.255.0',
    'vlan1': True,
    'vlan1_ip_addr': '10.220.89.1',
    'vlan1_netmask': '255.255.255.0',
}

template_file = 'intf_config2.j2'
template = env.get_template(template_file)
output = template.render(**intf_vars)
print(output)
