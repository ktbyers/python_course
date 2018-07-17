#!/usr/bin/env python
"""
Use the pynxos library and NX-API to retreive the output of 'show ip route vrf management' from the
nxos1 switch.

Parse the returned data structure and from this, retrieve the next hop for the
default route. Print this to standard output.
"""
from __future__ import print_function, unicode_literals
from pynxos.device import Device
from getpass import getpass

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def process_route_table(route_table):
    """Strip off unneeeded header information."""
    route_table = route_table['TABLE_vrf']['ROW_vrf']['TABLE_addrf']['ROW_addrf']
    return route_table['TABLE_prefix']['ROW_prefix']


def extract_next_hop(route_entry):
    route_data = route_entry['TABLE_path']['ROW_path']
    return route_data['ipnexthop']


def main():
    password = getpass()
    nxos1 = {
        'host': 'nxos1.twb-tech.com',
        'username': 'pyclass',
        'password': password,
        'transport': 'https',
        'port': 8443,
    }
    nxos2 = {   # noqa
        'host': 'nxos2.twb-tech.com',
        'username': 'pyclass',
        'password': password,
        'transport': 'https',
        'port': 8443,
    }

    print()
    for device in (nxos1,):
        nxapi_conn = Device(**device)
        print('-' * 40)
        route_table = nxapi_conn.show('show ip route vrf management')
        route_table = process_route_table(route_table)
        for route_entry in route_table:
            if route_entry['ipprefix'] == '0.0.0.0/0':
                next_hop = extract_next_hop(route_entry)
                print("Default Gateway: {}".format(next_hop))
                break
        print('-' * 40)
    print()


if __name__ == "__main__":
    main()
