#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader('.')

device_vars = {}

template_file = 'cisco1_config_2.j2'
template = env.get_template(template_file)
print(template.render(device_vars))
