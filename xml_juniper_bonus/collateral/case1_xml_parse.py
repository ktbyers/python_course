from __future__ import unicode_literals, print_function
from lxml import etree

with open('show_version.xml') as f:
    my_tree = etree.fromstring(f.read())

print(my_tree)
