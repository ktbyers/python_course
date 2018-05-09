#!/usr/bin/env python
"""Accomplish class #8, exercise1b using a script"""
from __future__ import print_function, unicode_literals
import django
django.setup()
from net_system.models import NetworkDevice, Credentials    # noqa


def main():
    """Link credentials to devices"""
    net_devices = NetworkDevice.objects.all()
    creds = Credentials.objects.all()

    std_creds = creds[0]
    arista_creds = creds[1]

    for a_device in net_devices:
        if 'arista' in a_device.device_type:
            a_device.credentials = arista_creds
        else:
            a_device.credentials = std_creds
        a_device.save()

    for a_device in net_devices:
        print(a_device, a_device.credentials)


if __name__ == "__main__":
    main()
