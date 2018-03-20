#!/usr/bin/env python
"""
Convert the code from exercise2 to a class-based solution

This program is meaningfully more complicated in PY3, than PY2. Also it
is more complicated if you need both PY2 and PY3 compatibility.
"""
from __future__ import print_function, unicode_literals

import telnetlib
import time
import socket
import sys
import getpass

TELNET_PORT = 23
TELNET_TIMEOUT = 6


def write_bytes(out_data):
    """Write Python2 and Python3 compatible byte stream.

    This is a bit compliated :-(

    It basically ensures that the unicode in your program is always encoded into an UTF-8 byte
    stream in the proper way (when bytes are written out to the network).

    Or worded another way, Unicode in the program is in the idealized unicode code points, and
    when you write it out to the network it needs represented a certain way (encoded).
    """
    if sys.version_info[0] >= 3:
        if isinstance(out_data, type(u'')):
            return out_data.encode('utf-8')
        elif isinstance(out_data, type(b'')):
            return out_data
    else:
        if isinstance(out_data, type(u'')):
            return out_data.encode('utf-8')
        elif isinstance(out_data, type(str(''))):
            return out_data
    msg = "Invalid value for out_data neither unicode nor byte string: {}".format(out_data)
    raise ValueError(msg)


class TelnetConn(object):
    """Establish and manage telnet connection to network devices."""
    def __init__(self, ip_addr, username, password):
        self.ip_addr = ip_addr
        self.username = username
        self.password = password

        try:
            self.remote_conn = telnetlib.Telnet(self.ip_addr, TELNET_PORT, TELNET_TIMEOUT)
        except socket.timeout:
            sys.exit("Connection timed-out")

    def write_channel(self, data):
        """Handle the PY2/PY3 differences to write data out to the device."""
        self.remote_conn.write(write_bytes(data))

    def read_channel(self):
        """Handle the PY2/PY3 differences to write data out to the device."""
        return self.remote_conn.read_very_eager().decode('utf-8', 'ignore')

    def login(self):
        """Login to network device."""
        output = self.remote_conn.read_until(b"sername:", TELNET_TIMEOUT).decode('utf-8', 'ignore')
        self.write_channel(self.username + '\n')
        output += self.remote_conn.read_until(b"ssword:", TELNET_TIMEOUT).decode('utf-8', 'ignore')
        self.write_channel(self.password + '\n')
        time.sleep(1)
        return output

    def send_command(self, cmd="\n", sleep_time=1):
        """
        Send a command down the telnet channel

        Return the response
        """
        cmd = cmd.rstrip()
        self.write_channel(cmd + '\n')
        time.sleep(sleep_time)
        return self.read_channel()

    def disable_paging(self, paging_cmd='terminal length 0'):
        """Disable the paging of output."""
        return self.send_command(paging_cmd)

    def close_conn(self):
        """Close telnet connection"""
        self.remote_conn.close()
        self.remote_conn = None


def main():
    """Convert the code from exercise2 to a class-based solution."""
    try:
        ip_addr = raw_input("IP address: ")
    except NameError:
        ip_addr = input("IP address: ")
    ip_addr = ip_addr.strip()
    username = 'pyclass'
    password = getpass.getpass()

    my_conn = TelnetConn(ip_addr, username, password)
    my_conn.login()
    my_conn.send_command()
    my_conn.disable_paging()
    output = my_conn.send_command('show ip int brief')

    print("\n\n")
    print(output)
    print("\n\n")

    my_conn.close_conn()


if __name__ == "__main__":
    main()
