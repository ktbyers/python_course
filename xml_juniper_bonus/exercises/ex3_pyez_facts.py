#!/usr/bin/env python
"""Connect to Juniper device using PyEZ. Display device facts."""
from __future__ import print_function, unicode_literals

from jnpr.junos import Device
from getpass import getpass
from pprint import pprint


def main():
    """Connect to Juniper device using PyEZ. Display device facts."""
    pwd = getpass()
    try:
        ip_addr = raw_input("Enter Juniper SRX IP: ")
    except NameError:
        ip_addr = input("Enter Juniper SRX IP: ")
    ip_addr = ip_addr.strip()

    juniper_srx = {
        "host": ip_addr,
        "user": "pyclass",
        "password": pwd
    }

    print("\n\nConnecting to Juniper SRX...\n")
    a_device = Device(**juniper_srx)
    a_device.open()
    pprint(a_device.facts)
    print()


if __name__ == "__main__":
    main()
