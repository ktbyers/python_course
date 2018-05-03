#!/usr/bin/env python
"""Test NAPALM config merge operations on one of the Cisco routers."""
from __future__ import print_function, unicode_literals

from napalm import get_network_driver
from my_devices import pynet_rtr1, pynet_sw1, nxos1

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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

        template_vars = {
            'dns1': '1.1.1.1',
            'dns2': '8.8.8.8',
        }

        device_type = a_device.pop('device_type')

        # NAPALM load_template requires an absolute path
        base_dir = '/home/kbyers/python_course/class7/CFGS/'

        print()
        print('-' * 50)
        print("Platform: {}".format(device_type))
        print(">>>Device open")
        driver = get_network_driver(device_type)
        device = driver(**a_device)
        device.open()

        print()
        print(">>>Commit change")
        device.load_template("dns", template_path=base_dir, **template_vars)
        print(device.compare_config())
        device.commit_config()

        ping_google(device)
        print("\n\n")

    print()


if __name__ == "__main__":
    main()
