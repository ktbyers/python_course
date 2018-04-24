from __future__ import print_function, unicode_literals
from rpc_client import RPCClient
from getpass import getpass
from pprint import pprint

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

device = RPCClient(host='nxos1.twb-tech.com',
                   username='pyclass',
                   password=getpass(),
                   transport='https',
                   port=8443,
                   verify=False)     # Don't verify SSL cert

# response = device.send_request(commands=['show version'], method='cli_ascii')
response = device.send_request(commands=['show version'], method='cli')
pprint(response)
