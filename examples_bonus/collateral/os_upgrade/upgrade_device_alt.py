#!/usr/bin/env python
"""
Alternate solution to the OS Upgrade Example. This was the one I created during my initial
planning and experimentation.
"""
from __future__ import print_function, unicode_literals
from getpass import getpass
from datetime import datetime
import re
import sys

from netmiko import ConnectHandler, file_transfer


def hit_any_key():
    try:
        raw_input("Hit any key to continue: ")
    except NameError:
        input("Hit any key to continue: ")


def verify_image(ssh_conn, file_system, dest_file, file_size):
    verify_cmd = 'dir {}/{}'.format(file_system, dest_file)
    verify_output = ssh_conn.send_command(verify_cmd)
    if file_size in verify_output and dest_file in verify_output:
        print()
        print(">>>>>")
        print("The new image is on the remote device:")
        print(verify_output)
        print(">>>>>")
        print()
        hit_any_key()
    else:
        raise ValueError("New image not detected on remote device.")


def check_boot_var(ssh_conn):
    """Currently only handles a single boot system statement."""
    current_boot = ssh_conn.send_command("show run | inc boot")
    match = re.search(r"^(boot system flash .*)$", current_boot, flags=re.M)
    boot_cmd = ''
    if match:
        boot_cmd = match.group(1)
    return boot_cmd


def upgrade_device(net_device):

    start_time = datetime.now()

    print()
    print("Upgrading OS on device: {}".format(net_device['host']))
    print("-" * 50)

    # Extract file and file system variables
    file_system = net_device.pop('file_system')
    source_file = net_device.pop('source_file')
    dest_file = net_device.pop('dest_file')

    # Establish SSH control channel
    print(".establishing SSH connection.")
    ssh_conn = ConnectHandler(**net_device)

    # SCP new image file
    print(".transferring image file.")
    enable_transfer = True
    if enable_transfer:
        transfer_dict = file_transfer(ssh_conn, source_file=source_file, dest_file=dest_file,
                                      file_system=file_system, direction='put',
                                      overwrite_file=False)
    else:
        transfer_dict = {}

    # Check the file exists and the MD5 matches the source file
    if not transfer_dict.get('file_exists') or not transfer_dict.get('file_verified'):
        raise ValueError("File doesn't exist or MD5 doesn't match on the remote system")

    print(".verifying new image file.")
    file_size = '42628912'
    verify_image(ssh_conn, file_system, dest_file, file_size)
    print()

    print(".checking current boot commands")
    boot_cmd = check_boot_var(ssh_conn)

    print(".constructing new boot commands")
    if boot_cmd:
        boot_commands = [
            "no {}".format(boot_cmd),
            'boot system flash {}'.format(dest_file),
            boot_cmd,
        ]
    else:
        boot_commands = [
            'boot system flash {}'.format(dest_file),
        ]

    print()
    print(">>>>>")
    print("Boot commands to send to the remote device:")
    print(boot_commands)
    print(">>>>>")
    print()
    hit_any_key()

    print()
    print(".sending new boot commands to remote device.")
    output = ssh_conn.send_config_set(boot_commands)
    print()

    print()
    print("Current boot variable: ")
    print(">>>>>")
    current_boot = ssh_conn.send_command("show run | inc boot")
    print(current_boot)
    print(">>>>>")
    print()

    # Reload the device
    print()
    try:
        response = raw_input("Do you want to reload the device(y/n): ")
    except NameError:
        response = input("Do you want to reload the device(y/n): ")

    if response.lower() != 'y':
        sys.exit("Boot commands staged, but device not reloaded!\n\n")
    else:
        print("Saving running-config to startup-config")
        ssh_conn.save_config()
        print("Reloading device with new image!")
        output = ssh_conn.send_command_timing("reload")
        print(output)
        if 'confirm' in output:
            output = ssh_conn.send_command_timing("y")

    end_time = datetime.now()
    print("File transfer time: {}".format(end_time - start_time))


if __name__ == "__main__":

    password = getpass()

    cisco1 = {
        'device_type': 'cisco_ios',
        'host': 'cisco1.twb-tech.com',
        'username': 'pyclass',
        'password': password,
        'file_system': 'flash:',
        'source_file': 'test1.bin',
        'dest_file': 'test1.bin',
    }

    for net_device in (cisco1,):
        upgrade_device(net_device)
