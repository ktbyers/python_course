#!/usr/bin/env python
"""
Update exercise2 such that you store the definition for the four Arista devices in an external
YAML file that you read in and parse upon script execution.

You should use the device definition in this external YAML file to make the Netmiko connections.
In other words, make your key-value pairs in your YAML dictionary match the key-value pairs that
you require for Netmiko.

Don't include the password in your YAML file. Add the password file using getpass() to the device
dictionary inside of your Python program.
"""
from __future__ import print_function, unicode_literals
from getpass import getpass
import yaml
from netmiko import ConnectHandler, file_transfer


def read_yaml(filename):
    with open(filename) as f:
        return yaml.load(f)


def main():
    password = getpass()

    filename = 'my_devices.yml'
    my_devices = read_yaml(filename)

    for hostname, net_device in my_devices.items():
        file_system = net_device.pop('file_system')
        net_device['password'] = password

        # Create the Netmiko SSH connection
        ssh_conn = ConnectHandler(**net_device)
        print()
        print(">>>>>")
        print(ssh_conn.find_prompt())

        # Transfer the IOS image to device
        source_file = "my_file.txt"
        dest_file = "my_file.txt"

        transfer_dict = file_transfer(
            ssh_conn,
            source_file=source_file,
            dest_file=dest_file,
            file_system=file_system,
            direction='put',
            overwrite_file=False,
        )

        md5_check = transfer_dict['file_verified']
        file_exists = transfer_dict['file_exists']

        if md5_check and file_exists:
            print("File successfully transferred to: {host}".format(**net_device))
        else:
            print("Failure on SCP: {host} !!!".format(**net_device))
        print(">>>>>")


if __name__ == "__main__":
    main()
