#!/usr/bin/env python
"""
Use the pynxos library to configure a loopback interface on nxos1. Choose a random
loopback interface number between 1 and 99.

Assign the loopback interface an IP address in the 172.16.0.0 - 172.31.255.255. Use
a /32 netmask.

Execute a 'show run interface loopbackX' command using NX-API to verify your interface
was configured properly. For example:

nxapi_conn.show('show run interface loopback99', raw_text=True)

Note, you will need to use 'raw_text=True' for this command.
"""
from __future__ import print_function, unicode_literals
from pynxos.device import Device
from getpass import getpass

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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

    config_commands = ['interface Loopback99', 'ip address 172.31.254.99/32']
    for device in (nxos1,):
        nxapi_conn = Device(**device)
        nxapi_conn.config_list(config_commands)
        output = nxapi_conn.show('show run interface loopback99', raw_text=True)
        print(output)


if __name__ == "__main__":
    main()
