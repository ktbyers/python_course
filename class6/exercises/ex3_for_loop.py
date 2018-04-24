#!/usr/bin/env python
"""
Expand upon exercise2 to generate the following:

--------

interface Loopback0
 ip address 172.31.255.1 255.255.255.255

router ospf 40
 network 10.220.88.0 0.0.0.255 area 0
 network 172.31.255.28 0.0.0.0 area 1

--------

The Jinja2 template should be read from an external file named 'ospf_config_for.j2'.

The OSPF 'network' statements should be generated using a for-loop embedded in the Jinja2
template. 

You should have a Python data structure named 'ospf_networks' that you iterate over (in your
Jinja2). At the highest-level this data structure should be either a list or a dictionary.

The following items should all be variables in the template:
process_id
network*         # Contained inside of ospf_networks variable (inside for-loop)
wildcard*        # Contained inside of ospf_networks variable (inside for-loop)
area*            # Contained inside of ospf_networks variable (inside for-loop)
loopback0_addr
loopback0_maks

Additionally, the interface Loopback0 and its ip address config should only be generated
if the loopback0_addr variable is defined (i.e. use an if-condition here).

"""
from __future__ import print_function, unicode_literals
import jinja2

filename = 'ospf_config_for.j2'
with open(filename) as f:
    ospf_template = f.read()

ospf_networks = [
    {
        'network': '10.220.88.0',
        'wildcard': '0.0.0.255',
        'area': 0,
    },
    {
        'network': '172.31.255.28',
        'wildcard': '0.0.0.0',
        'area': 1,
    },
]

ospf_vars = {
    'process_id': 40,
    'ospf_networks': ospf_networks,
    'loopback0_addr': '172.31.255.1',
    'loopback0_mask': '255.255.255.255',
}

template = jinja2.Template(ospf_template)
output = template.render(**ospf_vars)
print(output)
