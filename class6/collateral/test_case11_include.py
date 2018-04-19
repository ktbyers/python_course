#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader('.')

bgp_vars = {
    "hostname": "test-rtr1",
    "local_as": 10,
    "peer1_ip": "10.255.255.2",
    "peer1_as": 20,
    "advertised_route1": "10.10.200.0/24",
    "advertised_route2": "10.10.201.0/24",
    "advertised_route3": "10.10.202.0/24",
}

template_file = 'nxos_bgp_include.j2'
template = env.get_template(template_file)
print(template.render(bgp_vars))
