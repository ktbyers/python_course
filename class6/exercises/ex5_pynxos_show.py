#!/usr/bin/env python
"""
Use the pynxos library to create an NX-API connection to both nxos1.twb-tech.com and to
nxos2.twb-tech.com.

Use the pynxos 'show' method to retrieve 'show hostname' from each of the devices.
Print this show hostname output to standard output.
"""
from __future__ import print_function, unicode_literals
from pynxos.device import Device
from getpass import getpass

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

password = getpass()
nxos1 = {
    'host': 'nxos1.twb-tech.com',
    'username': 'pyclass',
    'password': password,
    'transport': 'https',
    'port': 8443,
}
nxos2 = {
    'host': 'nxos2.twb-tech.com',
    'username': 'pyclass',
    'password': password,
    'transport': 'https',
    'port': 8443,
}

print()
for device in (nxos1, nxos2):
    nxapi_conn = Device(**device)
    print('-' * 40)
    print(nxapi_conn.show('show hostname'))
    print('-' * 40)
print()
