#!/usr/bin/env python
from __future__ import unicode_literals, print_function
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader('.')

modules = [1, 2, 3, 4, 6, 7]
intf_vars = {
    'modules': modules,
    'port_count': 48,
    'vlan': 550,
}

template_file = 'switch_interfaces3.j2'
template = env.get_template(template_file)
output = template.render(**intf_vars)
print(output)
