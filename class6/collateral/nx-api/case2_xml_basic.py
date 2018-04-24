from __future__ import print_function, unicode_literals
from xml_client import XMLClient
from getpass import getpass

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

device = XMLClient(host='nxos1.twb-tech.com',
                   username='pyclass',
                   password=getpass(),
                   transport='https',
                   port=8443,
                   verify=False)     # Don't verify SSL cert

response = device.send_request(commands=['show version'], method='cli_show')
print()
print('#' * 80)
print(response)
print('#' * 80)
