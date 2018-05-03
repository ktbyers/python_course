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


def generate_config(loader_dir):
    """Generate the device configuration from a template."""
    jinja_env = Environment(undefined=StrictUndefined)
    template_vars = {
        'dns1': '1.1.1.1',
        'dns2': '8.8.8.8',
    }
    template_file = 'dns.j2'

    jinja_env.loader = FileSystemLoader(loader_dir)
    template = jinja_env.get_template(template_file)
    return template.render(template_vars)


def ping_google(device):
    "Use NAPALM to ping google.com to validate DNS resolution."""
    print()
    print(">>>Test ping to google.com")
    try:
        ping_output = device.ping(destination='google.com')
    except NotImplementedError:
        print("Ping failed: ping() method not implemented")
        return
    if not ping_output == {}:
        probes_sent = int(ping_output['success']['probes_sent'])
        packet_loss = int(ping_output['success']['packet_loss'])
        successful_pings = probes_sent - packet_loss
        print("Probes sent: {}".format(probes_sent))
        print("Packet loss: {}".format(packet_loss))
        if successful_pings > 0:
            print("Pings Successful: {}".format(successful_pings))
            return

    print("Ping failed")


def main():
    """Test NAPALM config merge operations on one of the Cisco routers."""

    for a_device in (pynet_rtr1, pynet_sw1, nxos1):
        device_type = a_device.pop('device_type')

        # Directory where template and config file will be stored
        base_dir = './CFGS/{}'.format(device_type)
        dns_file = '{}/dns.txt'.format(base_dir)

        # Generate config file from a template
        dns_output = generate_config(loader_dir=base_dir)

        # Write generated config to file
        with open(dns_file, 'w') as f:
            f.write(dns_output)

        print()
        print('-' * 50)
        print("Platform: {}".format(device_type))
        print(">>>Device open")
        driver = get_network_driver(device_type)
        device = driver(**a_device)
        device.open()

        print()
        print(">>>Commit change")
        device.load_merge_candidate(filename=dns_file)
        print(device.compare_config())
        device.commit_config()

        ping_google(device)
        print("\n\n")

    print()


if __name__ == "__main__":
    main()
