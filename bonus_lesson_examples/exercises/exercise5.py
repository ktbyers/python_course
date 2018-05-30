#!/usr/bin/env python
"""
Create NAPALM a script that connects to srx1 and retrieves its LLDP information
(get_lldp_neighbors() method).

From this returned data structure retrieve the local interface name, the remote switch name that
this srx1 is connected to, and the remote port name.

Email this local interface, remote switch name, and remote port name to yourself using the
send_mail function from earlier in the course.
"""
from __future__ import print_function, unicode_literals
from getpass import getpass
from napalm import get_network_driver
from email_helper import send_mail


def main():
    password = getpass()

    srx1 = {
        'device_type': 'junos',
        'hostname': 'srx1.twb-tech.com',
        'username': 'pyclass',
        'password': password,
        'optional_args': {},
    }

    for net_device in (srx1,):
        device_type = net_device.pop('device_type')
        driver = get_network_driver(device_type)

        # Establish a NAPALM connection
        device = driver(**net_device)
        device.open()
        lldp_neighbors = device.get_lldp_neighbors()

        # Should only be one entry
        for local_intf, lldp_list in lldp_neighbors.items():
            remote_lldp = lldp_list[0]
            remote_host = remote_lldp['hostname']
            remote_port = remote_lldp['port']
            break

        # Send email
        msg = """
SRX1 is connected on local intf: {local_intf}

To remote host: {remote_host}
On remote port: {remote_port}
""".format(local_intf=local_intf, remote_host=remote_host, remote_port=remote_port)

        recipient = 'ktbyers@twb-tech.com'
        sender = 'twb@twb-tech.com'
        subject = 'Bonus lesson LLDP exercise'
        send_mail(recipient, subject, message=msg, sender=sender)
        print()
        print("Message sent...check your inbox.")
        print()


if __name__ == "__main__":
    main()
