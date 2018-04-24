from __future__ import print_function, unicode_literals
from pynxos.device import Device
from getpass import getpass
from pprint import pprint

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

device = Device(host='nxos2.twb-tech.com',
                username='pyclass',
                password=getpass(),
                transport='https',
                port=8443)

print(device.show('show hostname'))

# Show command
command = 'show version'
output = device.show(command)
pprint(output)

# Show comand with raw_text i.e. unstructured data
command = 'show version'
output = device.show(command, raw_text=True)
print(output)

# Config command
commands = [
    'logging history size 300',
]
device.config_list(commands)

# Copy run to start
results = device.save()

# Method to create a checkpoint file

# Method to rollback to checkpoint file

# reboot method

# set_boot_options method

# Automatic facts
pprint(device.facts)

# FileCopy class and SCP capabilities
