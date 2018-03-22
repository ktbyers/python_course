#!/usr/bin/env python
"""
Using SNMPv3 create a script that detects router configuration changes.

If the running configuration has changed, then send an email notification to
yourself identifying the router that changed and the time that it changed.

In this exercise, you will possibly need to save data to an external file. Use
either JSON or YAML to save the data to an external file.
"""
from __future__ import print_function, unicode_literals

try:
    # PY2
    import cPickle as pickle
except ModuleNotFoundError:
    # PY3
    import pickle

import os.path
from datetime import datetime
from getpass import getpass
from collections import namedtuple

import json
import yaml

from snmp_helper import snmp_get_oid_v3, snmp_extract
from email_helper import send_mail


# Create namedtuple for network devices
NetworkDevice = namedtuple("NetworkDevice", "uptime last_changed run_config_changed")


def obtain_saved_objects(file_name):
    """
    Read in previously saved objects from a file

    Determine from the file_name whether .pkl, .yml, or .json, properly retrieve the data from
    the file.

    Return the retrieved network devices
    """
    net_devices = {}

    # Check that the file exists
    if not os.path.isfile(file_name):
        return {}

    # Determine whether .pkl, .yml, or .json file
    if file_name.count(".") == 1:
        _, out_format = file_name.split(".")
    else:
        raise ValueError("Invalid file name: {0}".format(file_name))

    if out_format == 'pkl':
        with open(file_name, 'rb') as f:
            while True:
                try:
                    net_devices = pickle.load(f)
                except EOFError:
                    break
    elif out_format == 'yml':
        with open(file_name, 'r') as f:
            net_devices = yaml.load(f)
    elif out_format == 'json':
        with open(file_name, 'r') as f:
            net_devices = json.load(f)

            # JSON returns straight tuple, convert to namedtuple
            for device_name, device_attrs in net_devices.items():
                uptime, last_changed, run_config_changed = device_attrs
                tmp_device = NetworkDevice(uptime, last_changed, run_config_changed)
                net_devices[device_name] = tmp_device
    else:
        raise ValueError("Invalid file name: {}".format(file_name))
    return net_devices


def save_objects_to_file(file_name, data_dict):
    """Write the network devices out to a file."""

    # Determine whether .pkl, .yml, or .json file
    if file_name.count(".") == 1:
        _, out_format = file_name.split(".")
    else:
        raise ValueError("Invalid file name: {}".format(file_name))

    if out_format == 'pkl':
        with open(file_name, 'wb') as f:
            pickle.dump(data_dict, f)
    elif out_format == 'yml':
        with open(file_name, 'w') as f:
            f.write(yaml.dump(data_dict, default_flow_style=False))
    elif out_format == 'json':
        with open(file_name, 'w') as f:
            json.dump(data_dict, f)


def send_notification(device_name):
    """Send email notification regarding modified device."""

    current_time = datetime.now()

    sender = 'sender@twb-tech.com'
    recipient = 'recipient@twb-tech.com'
    subject = 'Device {} was modified'.format(device_name)
    message = '''
The running configuration of {} was modified.

This change was detected at: {}

'''.format(device_name, current_time)

    if send_mail(recipient, subject, message, sender):
        print('Email notification sent to {}'.format(recipient))
        return True


def get_snmp_system_name(a_device, snmp_user):
    """Use SNMP to obtain the system name."""
    sys_name_oid = '1.3.6.1.2.1.1.5.0'
    return snmp_extract(snmp_get_oid_v3(a_device, snmp_user, oid=sys_name_oid))


def get_snmp_uptime(a_device, snmp_user):
    """Use SNMP to obtain the system uptime."""
    sys_uptime_oid = '1.3.6.1.2.1.1.3.0'
    return int(snmp_extract(snmp_get_oid_v3(a_device, snmp_user, oid=sys_uptime_oid)))


def create_new_device(device_name, uptime, last_changed):
    """Create new Network Device."""
    dots_to_print = (35 - len(device_name)) * '.'
    print("{} {}".format(device_name, dots_to_print), end=' ')
    print("saving new device")
    return NetworkDevice(uptime, last_changed, False)


def check_for_reboot(saved_device, uptime, last_changed):
    """Check if the network devices has rebooted."""
    # Did uptime decrease or did last_changed decrease
    return uptime < saved_device.uptime or last_changed < saved_device.last_changed


def main():
    """
    Check if the running-configuration has changed, send an email notification when
    this occurs.

    Logic for detecting the running-config has changed:

        Normal (non-reboot):

            # Did RUN_LAST_CHANGED increase
            if RUN_LAST_CHANGED > network_device_object.last_changed:
                config_changed = True

        Reboot case:

            RUN_LAST_CHANGED decreases (i.e. < network_device_object.last_changed)

            Right after reboot, RUN_LAST_CHANGED is updated upon
            load of running-config from startup-config.

            Create a grace window (RELOAD_WINDOW) for values of RUN_LAST_CHANGED.
            In other words as long as RUN_LAST_CHANGED is <= RELOAD_WINDOW assume
            no running-config changes.

            If RUN_LAST_CHANGED is > RELOAD_WINDOW assume running-config was changed
    """
    # 300 seconds (converted to hundredths of seconds)
    reload_window = 300 * 100

    # Uptime when running config last changed
    run_last_changed = '1.3.6.1.4.1.9.9.43.1.1.1.0'

    # File for storing previous RunningLastChanged timestamp
    net_dev_file = 'netdev.pkl'
    # net_dev_file = 'netdev.yml'
    # net_dev_file = 'netdev.json'

    try:
        rtr1_ip_addr = raw_input("Enter pynet-rtr1 IP: ")
        rtr2_ip_addr = raw_input("Enter pynet-rtr2 IP: ")
    except NameError:
        rtr1_ip_addr = input("Enter pynet-rtr1 IP: ")
        rtr2_ip_addr = input("Enter pynet-rtr2 IP: ")
    my_key = getpass(prompt="Auth + Encryption Key: ")

    # SNMPv3 Connection Parameters
    snmp_user = ('pysnmp', my_key, my_key)
    pynet_rtr1 = (rtr1_ip_addr, 161)
    pynet_rtr2 = (rtr2_ip_addr, 161)

    print('\n*** Checking for device changes ***')
    saved_devices = obtain_saved_objects(net_dev_file)
    print("{} devices were previously saved\n".format(len(saved_devices)))

    # Temporarily store the current devices in a dictionary
    current_devices = {}

    # Connect to each device / retrieve last_changed time
    for a_device in (pynet_rtr1, pynet_rtr2):
        device_name = get_snmp_system_name(a_device, snmp_user)
        uptime = get_snmp_uptime(a_device, snmp_user)
        last_changed = int(snmp_extract(snmp_get_oid_v3(a_device, snmp_user, oid=run_last_changed)))
        print("\nConnected to device = {}".format(device_name))
        print("Last changed timestamp = {}".format(last_changed))
        print("Uptime = {}".format(uptime))

        # New network device
        if device_name not in saved_devices:
            current_devices[device_name] = create_new_device(device_name, uptime, last_changed)
        else:
            # Device has been previously saved
            saved_device = saved_devices[device_name]
            dots_to_print = (35 - len(device_name)) * '.'
            print("{} {}".format(device_name, dots_to_print), end=' ')

            if check_for_reboot(saved_device, uptime, last_changed):
                # reload_window is to try to ensure enough delay so that running-config will be
                # loaded upon reload.
                if last_changed <= reload_window:
                    print("DEVICE RELOADED...not changed")
                    current_devices[device_name] = NetworkDevice(uptime, last_changed, False)
                else:
                    print("DEVICE RELOADED...and changed")
                    current_devices[device_name] = NetworkDevice(uptime, last_changed, True)
                    send_notification(device_name)

            # running-config did not change
            elif last_changed == saved_device.last_changed:
                print("not changed")
                current_devices[device_name] = NetworkDevice(uptime, last_changed, False)

            # running-config changed
            elif last_changed > saved_device.last_changed:
                print("CHANGED")
                current_devices[device_name] = NetworkDevice(uptime, last_changed, True)
                send_notification(device_name)
            else:
                raise ValueError()

    save_objects_to_file(net_dev_file, current_devices)
    print()


if __name__ == '__main__':
    main()
