#!/usr/bin/env python
"""

"""
from __future__ import print_function, unicode_literals
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader('.')

device_vars = {
    'hostname': 'pynet-sw4',
    'ntp1': '130.126.24.24',
    'vlan1_ip': '10.220.88.31/24',
    'gateway': '10.220.88.1',
}

template_file = 'arista_template.j2'
template = env.get_template(template_file)
print(template.render(device_vars))
