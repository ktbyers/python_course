#!/usr/bin/env python
"""
"""
from __future__ import print_function, unicode_literals
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader('.')

ospf_vars = {
    'process_id': 40,
    'router_id': '172.16.88.1',
    'area': '0.0.0.0',
}

template_file = 'ospf_config_include_3.j2'
template = env.get_template(template_file)
print(template.render(ospf_vars))
