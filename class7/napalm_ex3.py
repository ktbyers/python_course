#!/usr/bin/env python
"""
Using NAPALM retreive 'get_bgp_neighbors' from pynet-rtr1. Parse the returned data structure to and
verify that the BGP peer to 10.220.88.38 is in the established state ('is_up' field in the NAPALM
returned data structure).
"""
from __future__ import print_function, unicode_literals
from napalm import get_network_driver
from my_devices import pynet_rtr1


def retrive_bgp_neighbor(bgp_data, neighbor):
    """
    Parse the output from NAPALM's get_bgp_neighbors()

    Retrieve the specified neighbor's BGP dictionary.
    """
    return bgp_data['global']['peers'][neighbor]


def main():
    """
    Connect to set of network devices using NAPALM (different platforms); print
    out the facts.
    """
    for a_device in (pynet_rtr1,):
        device_type = a_device.pop('device_type')
        driver = get_network_driver(device_type)
        device = driver(**a_device)

        print()
        print(">>>Device open")
        device.open()

        print("-" * 50)
        hostname = a_device['hostname']
        print("{hostname}:\n".format(hostname=hostname))

        # Retrieve BGP information and parse returned data
        bgp_info = device.get_bgp_neighbors()
        bgp_neighbor = '10.220.88.38'
        bgp_neighbor_dict = retrive_bgp_neighbor(bgp_info, bgp_neighbor)
        bgp_state = bgp_neighbor_dict['is_up']
        print("BGP Neighbor: {}, BGP Established State: {}".format(bgp_neighbor, bgp_state))
        print()

    print()


if __name__ == "__main__":
    main()
