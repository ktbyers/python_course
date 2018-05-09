#!/usr/bin/env python
'''
Create two new test NetworkDevices in the database. Use both direct object creation
and the .get_or_create() method to create the devices.
'''
from __future__ import print_function, unicode_literals
import django
django.setup()
from net_system.models import NetworkDevice     # noqa


def main():
    '''
    Create two new test NetworkDevices in the database. Use both direct object creation
    and the .get_or_create() method to create the devices.
    '''
    try:
        ip_addr = raw_input("Enter IP address: ")
    except NameError:
        ip_addr = input("Enter IP address: ")

    test_rtr1 = NetworkDevice(
        device_name='test-rtr1',
        device_type='cisco_ios',
        ip_address=ip_addr,
        port=5022,
    )
    test_rtr1.save()

    # Create object for rtr2
    NetworkDevice.objects.get_or_create(
        device_name='test-rtr2',
        device_type='cisco_ios',
        ip_address=ip_addr,
        port=5122,
    )

    # Verify devices that currently exist
    print()
    devices = NetworkDevice.objects.all()
    for a_device in devices:
        print(a_device)
    print()


if __name__ == "__main__":
    main()
