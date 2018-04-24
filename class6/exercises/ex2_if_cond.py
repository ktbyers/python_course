#!/usr/bin/env python
"""
Expand upon exercise1 to generate the following:

--------

interface Loopback0
 ip address 172.31.255.1 255.255.255.255

router ospf 40
 network 10.220.88.0 0.0.0.255 area 0

--------

The Jinja2 template should be read from an external file named 'ospf_config.j2'.

The following items should all be variables in the template: process_id, network, wildcard,
area, loopback0_addr, loopback0_mask.

Additionally, the 'interface Loopback0' and its ip address configuration should only be generated
if the loopback0_addr variable is defined (i.e. use an if-condition here).

"""
from __future__ import print_function, unicode_literals
import jinja2

filename = 'ospf_config.j2'
with open(filename) as f:
    ospf_template = f.read()

ospf_vars = {
    'process_id': 40,
    'network': '10.220.88.0',
    'wildcard': '0.0.0.255',
    'area': 0,
    'loopback0_addr': '172.31.255.1',
    'loopback0_mask': '255.255.255.255',
}

template = jinja2.Template(ospf_template)
output = template.render(**ospf_vars)
print(output)
