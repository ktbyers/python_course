#!/usr/bin/env python
from __future__ import print_function, unicode_literals
"""Test NAPALM config merge operations on one of the Cisco routers."""
from napalm import get_network_driver
from my_devices import pynet_rtr1, pynet_sw1, nxos1
import jinja2

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main():
    """Test NAPALM config merge operations on one of the Cisco routers."""
    for a_device in (pynet_rtr1, pynet_sw1, nxos1):
        device_type = a_device.pop('device_type')
        driver = get_network_driver(device_type)
        device = driver(**a_device)

        print()
        print(">>>Device open")
        device.open()

        dns_file = './CFGS/{}/dns.txt'.format(device_type)
        print()
        print(">>>Load config change (merge) - no commit")
        device.load_merge_candidate(filename=dns_file)
        print(device.compare_config())

    print()


if __name__ == "__main__":
    main()
