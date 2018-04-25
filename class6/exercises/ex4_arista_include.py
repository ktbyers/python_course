#!/usr/bin/env python
"""
Use Jinja2 templating to generate the following Arista configuration.

--------
!
hostname sanfran-sw4
!
ntp server 10.10.10.24
!
snmp-server contact Isaac Newton
snmp-server location San Francisco, CA
snmp-server community foo ro SNMP
!
spanning-tree mode mstp
!
aaa authorization exec default local
!
no aaa root
!
username local privilege 15 secret 5 $1$C3VxRxcO$71x9abDD09yW.NIR8d2Lh0
username admin privilege 15 secret 5 $1$C3VxRxcO$71x9abDD09yW.NIR8d2Lh0
!
clock timezone America/Los_Angeles
!
interface Ethernet1
   spanning-tree portfast
   spanning-tree cost 1
!
interface Ethernet2
!
interface Ethernet3
!
interface Ethernet4
!
interface Ethernet5
!
interface Ethernet6
!
interface Ethernet7
!
interface Management1
   shutdown
!
interface Vlan1
   ip address 10.10.88.31/24
!
ip route 0.0.0.0/0 10.10.88.1
!
ip routing
!
management api http-commands
   no shutdown
!
!
end
--------

The main template should be stored in an external file named 'arista_template.j2'.

This template should use the Jinja2 include statement to pull in two additional templates. The
first template should be named 'arista_users.j2' and should contain the two username statements.
The second template should be named 'snmp.j2' and should include all of the SNMP statments.

The SNMP location, contact, and community should all be made into Jinja2 variables. The rest of the
configuration can be hard-coded (i.e. you don't need any other variables besides those three SNMP
variables).

"""
from __future__ import print_function, unicode_literals
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader('.')

device_vars = {
    'snmp_location': 'San Francisco, CA',
    'snmp_contact': 'Isaac Newton',
    'snmp_community': 'foo',
}

template_file = 'arista_template.j2'
template = env.get_template(template_file)
print(template.render(device_vars))
