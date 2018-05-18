from __future__ import unicode_literals, print_function
from lxml import etree

with open('show_version.xml') as f:
    show_version = etree.fromstring(f.read())

print()
print("Our XML")
print("-" * 20)
print(etree.tostring(show_version, pretty_print=True).decode().rstrip())
print("-" * 20)
print()

print("Print the tag name of the root element:")
print("-" * 20)
print(show_version.tag)
print()

print("Access the child elements as list indices:")
print("-" * 20)
print(show_version[0].tag)
print(show_version[1].tag)
print(show_version[2].tag)
print(show_version[3].tag)
print(show_version[4].tag)
print(show_version[5].tag)
print()

print("Looping over the child elements:")
print("-" * 20)
for child in show_version:
    print(child.tag)
print()

print("You can also access attributes: ")
print("-" * 20)
host1 = show_version[0]
print("Model: {}".format(host1.get('model')))
print("Showing host1 .keys(): {}".format(host1.keys()))
print("Showing host1 .items(): {}".format(host1.items()))
print()

print("You can also access text nodes: ")
print("-" * 20)
print(host1.text)
print()
