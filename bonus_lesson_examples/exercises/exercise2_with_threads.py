#!/usr/bin/env python
"""
Create a file named 'my_file.txt' with some random content in it.

Use Netmiko's secure copy to transfer this file to the Arista1, Arista2, Arista3, and Arista4
switches.

Note, you will need to use PIP to upgrade Netmiko in the lab environment to Netmiko 2.1.1 to
complete this exercise:

pip install netmiko==2.1.1

At the end of the transfer make sure the file exists and the MD5 passed. Netmiko should report
this back to you as part of its file_transfer function.

Optional Bonus: Use threads so this transfer happens to all four switches concurrently.
"""
from __future__ import print_function, unicode_literals
import threading
from datetime import datetime
from getpass import getpass
from netmiko import ConnectHandler, file_transfer


def create_device_dict(hostname, password):
    return {
        'device_type': 'arista_eos',
        'host': hostname,
        'username': 'pyclass',
        'password': password,
        'file_system': "/mnt/flash",
    }


def scp_file(net_device):
    # Make a copy of the dictionary since we modify it
    device_dict = net_device.copy()
    file_system = device_dict.pop('file_system')

    # Create the Netmiko SSH connection
    ssh_conn = ConnectHandler(**device_dict)

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

    ssh_conn.disconnect()


def main():
    password = getpass()
    start_time = datetime.now()

    hostnames = [
        'arista1.twb-tech.com',
        'arista2.twb-tech.com',
        'arista3.twb-tech.com',
        'arista4.twb-tech.com',
    ]

    print()
    print(">>>>>")
    for host in hostnames:
        net_device = create_device_dict(host, password)
        my_thread = threading.Thread(target=scp_file, args=(net_device,))
        my_thread.start()

    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()
    print(">>>>>")

    print("\nElapsed time: " + str(datetime.now() - start_time))


if __name__ == "__main__":
    main()
