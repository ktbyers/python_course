#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import jinja2

my_vars = {
    "router1": "cisco 881, fremont, ca"
}

my_template = '''
{{ router1 }}
{{ "%30s %30s" | format(router1, "hello") }}
'''

'''
{{ router1 | upper }}
{{ router1 | capitalize }}
{{ router1 | center( 80) }}
{{ router1 | upper | center( 80) }}
{{ router2 | default('not defined') }}
'''

template = jinja2.Template(my_template)
print(template.render(my_vars))
