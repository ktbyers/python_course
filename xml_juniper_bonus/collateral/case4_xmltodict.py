from __future__ import unicode_literals, print_function
from lxml import etree
import xmltodict

with open('show_version.xml') as f:
    show_version = etree.fromstring(f.read())

print()
print("Our XML")
print("-" * 20)
print(etree.tostring(show_version, pretty_print=True).decode().rstrip())
print("-" * 20)
print()

show_version_dict = xmltodict.parse(etree.tostring(show_version, encoding='unicode'))
