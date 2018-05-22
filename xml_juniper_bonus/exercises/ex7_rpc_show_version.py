#!/usr/bin/env python
'''
Use Juniper's PyEZ and direct RPC to retrieve the XML for 'show version' from the Juniper SRX.

Print out this returned XML as a string using 'etree.tostring()'. Parse the returned XML to
retrieve the model from the device. Print this model number to the screen.
'''
from __future__ import print_function, unicode_literals

from lxml import etree
from getpass import getpass

from jnpr.junos import Device


def main():
    """Use Juniper PyEZ and direct RPC to retrieve the XML for 'show version' from the SRX."""
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

    # show version | display xml rpc
    # get-software-information
    show_version = a_device.rpc.get_software_information()
    print()
    print("Print show version XML out as a string (retrieved via PyEZ RPC):")
    print("-" * 20)
    print(etree.tostring(show_version, pretty_print=True).decode())
    model = show_version.xpath("product-model")[0].text
    print()
    print("-" * 20)
    print("SRX Model: {}".format(model))
    print()


if __name__ == "__main__":
    main()
