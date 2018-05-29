"""
pynet-sw1  (Arista EOS)
pynet-sw2  (Arista EOS)
pynet-sw3  (Arista EOS)
pynet-sw4  (Arista EOS)
"""
from getpass import getpass

std_pwd = getpass("Enter standard password: ")

arista1 = {
    'device_type': 'eos',
    'hostname': 'arista1.twb-tech.com',
    'username': 'pyclass',
    'password': std_pwd,
    'optional_args': {},
}

arista2 = {
    'device_type': 'eos',
    'hostname': 'arista2.twb-tech.com',
    'username': 'pyclass',
    'password': std_pwd,
    'optional_args': {},
}

arista3 = {
    'device_type': 'eos',
    'hostname': 'arista3.twb-tech.com',
    'username': 'pyclass',
    'password': std_pwd,
    'optional_args': {},
}

arista4 = {
    'device_type': 'eos',
    'hostname': 'arista4.twb-tech.com',
    'username': 'pyclass',
    'password': std_pwd,
    'optional_args': {},
}
