from __future__ import unicode_literals, print_function
from lxml import etree

with open('show_version.xml') as f:
    show_version = etree.fromstring(f.read())

print(show_version)
print(etree.tostring(show_version, pretty_print=True).decode())
