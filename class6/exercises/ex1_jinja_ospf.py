#!/usr/bin/env python
"""
Use Jinja2 to generate the following configuration:

--------
router ospf 40
 network 10.220.88.0 0.0.0.255 area 0
--------

The process ID, network, wildcard mask, and area should all be variables in the Jinja2 template.

Use a template directly embedded in your Python script.

"""
from __future__ import print_function, unicode_literals
import jinja2

ospf_template = """
router ospf {{ process_id }}
 network {{ network }} {{ wildcard }} area {{ area }}

"""

ospf_vars = {
    'process_id': 40,
    'network': '10.220.88.0',
    'wildcard': '0.0.0.255',
    'area': 0,
}

template = jinja2.Template(ospf_template)
output = template.render(**ospf_vars)
print(output)
