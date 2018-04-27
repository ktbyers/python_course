#!/usr/bin/env python
"""
Using NAPALM retrieve get_interfaces from Arista switch2 (pynet_sw2). Find all of the interfaces
that are in an UP-UP state (is_enabled=True, and is_up=True). Print all of these UP-UP interfaces
to standard output.
"""
from __future__ import print_function, unicode_literals
from napalm import get_network_driver
from my_devices import pynet_sw2


def check_up_up(intf_data):
    if intf_data['is_enabled'] and intf_data['is_up']:
        return True
    return False


def main():
    """Retrieve get_interfaces and find the up-up interfaces."""
    for a_device in (pynet_sw2,):
        device_type = a_device.pop('device_type')
        driver = get_network_driver(device_type)
        device = driver(**a_device)

        print()
        print(">>>Device open")
        device.open()

        print("-" * 50)
        hostname = a_device['hostname']
        print("{hostname}:\n".format(hostname=hostname))

        intf_info = device.get_interfaces()

        print()
        print("UP-UP Interfaces: ")
        print("-" * 50)
        intf_list = []
        for intf_name, intf_data in intf_info.items():
            if check_up_up(intf_data):
                intf_list.append(intf_name)

        # Sort by nam
        intf_list.sort()
        for intf in intf_list:
            print(intf)

    print()


if __name__ == "__main__":
    main()
