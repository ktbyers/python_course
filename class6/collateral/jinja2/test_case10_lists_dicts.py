#!/usr/bin/env python
from __future__ import unicode_literals, print_function
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader('.')

modules = {
    1: {'default_vlan': 520, 'ports': range(1, 25)},
    2: {'default_vlan': 530, 'ports': range(1, 49)},
    3: {'default_vlan': 540, 'ports': range(1, 49)},
    4: {'default_vlan': 600, 'ports': range(1, 25)},
}

intf_vars = {
    'modules': modules,
}

template_file = 'switch_interfaces4.j2'
template = env.get_template(template_file)
output = template.render(**intf_vars)
print(output)
