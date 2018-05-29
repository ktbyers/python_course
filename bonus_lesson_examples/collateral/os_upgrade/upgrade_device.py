#!/usr/bin/env python
from getpass import getpass
from netmiko import ConnectHandler, file_transfer
import re


def any_key():
    try:
        raw_input("Hit any key to continue: ")
    except NameError:
        input("Hit any key to continue: ")
    print()


def main():

    password = getpass()

    cisco1 = {
        'device_type': 'cisco_ios',
        'host': 'cisco1.twb-tech.com',
        'username': 'pyclass',
        'password': password,
        'file_system': 'flash:'
    }

    for net_device in (cisco1,):

        file_system = net_device.pop('file_system')

        # Create the Netmiko SSH connection
        ssh_conn = ConnectHandler(**net_device)
        print(ssh_conn.find_prompt())

        # Transfer the IOS image to device
        source_file = "test1.bin"
        dest_file = "test1.bin"
        scp_transfer = False
        if scp_transfer:
            transfer_dict = file_transfer(
                ssh_conn,
                source_file=source_file,
                dest_file=dest_file,
                file_system=file_system,
                direction='put',
                overwrite_file=False,
            )

            if not transfer_dict['file_exists'] or not transfer_dict['file_verified']:
                raise ValueError("The SCP file transfer failed.")

        else:
            transfer_dict = {}

        print(transfer_dict)
        any_key()

        # Verifying the file transferred correctly
        dir_cmd = "dir {}/{}".format(file_system, dest_file)
        output = ssh_conn.send_command(dir_cmd)

        if '42628912' not in output or dest_file not in output:
            raise ValueError("The SCP file transfer failed.")
        print(output)
        any_key()

        output = ssh_conn.send_command("show run | inc boot")
        print(output)
        any_key()

        # boot system flash c880data-universalk9-mz.154-2.T1.bin
        match = re.search("^(boot system flash .*.bin)$", output, flags=re.M)
        if match:
            current_boot = match.group(1)

        # Construct a new boot variable
        config_cmds = [
            'no {}'.format(current_boot),
            'boot system flash test1.bin',
            current_boot,
        ]

        output = ssh_conn.send_config_set(config_cmds)

        show_boot = ssh_conn.send_command("show run | inc boot")
        ssh_conn.save_config()
        print(show_boot)
        any_key()

        output = ssh_conn.send_command_timing("reload")
        if 'confirm' in output:
            output += ssh_conn.send_command_timing("y")


if __name__ == "__main__":
    main()
