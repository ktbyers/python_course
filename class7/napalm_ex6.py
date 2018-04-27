#!/usr/bin/env python
"""Test NAPALM config merge operations on one of the Cisco routers."""
from __future__ import print_function, unicode_literals

from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

from napalm import get_network_driver
from my_devices import pynet_rtr1, pynet_sw1, nxos1

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def main():
    """Test NAPALM config merge operations on one of the Cisco routers."""
    env = Environment(undefined=StrictUndefined)
    template_vars = {
        'dns1': '1.1.1.1',
        'dns2': '8.8.8.8',
    }
    template_file = 'dns.j2'

    for a_device in (pynet_rtr1, pynet_sw1, nxos1):
        device_type = a_device.pop('device_type')
        driver = get_network_driver(device_type)
        device = driver(**a_device)

        base_dir = './CFGS/{}'.format(device_type)
        dns_file = '{}/dns.txt'.format(base_dir)
        env.loader = FileSystemLoader(base_dir)

        template = env.get_template(template_file)
        dns_output = (template.render(template_vars))
        with open(dns_file, 'w') as f:
            f.write(dns_output)

        print()
        print(">>>Device open")
        device.open()

        print()
        print(">>>Commit change")
        device.load_merge_candidate(filename=dns_file)
        print(device.compare_config())
        device.commit_config()

        ping_output = device.ping(destination='google.com')
        print(ping_output)

    print()


if __name__ == "__main__":
    main()
