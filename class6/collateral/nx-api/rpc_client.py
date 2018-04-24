"""
Based upon RPCClient object in pynxos libary.
"""
from __future__ import unicode_literals, print_function
import requests
from requests.auth import HTTPBasicAuth
import json


class RPCClient(object):
    def __init__(self, host, username, password, transport='https', port=None, verify=True):
        if transport not in ['http', 'https']:
            raise ValueError("'{}' is an invalid transport.".format(transport))

        if port is None:
            if transport == 'http':
                port = 80
            elif transport == 'https':
                port = 443

        self.url = '%s://%s:%s/ins' % (transport, host, port)
        self.headers = {u'content-type': u'application/json-rpc'}
        self.username = username
        self.password = password
        self.verify = verify

    def _build_payload(self, commands, method, rpc_version='2.0', version=1):
        """Build the JSON-RPC payload.

        Example payload:
        [
          {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
              "cmd": "show ip arp",
              "version": 1.2
            },
            "id": 1
          }
        ]

        """
        payload_list = []
        id_num = 1
        for command in commands:
            payload = dict(jsonrpc=rpc_version,
                           method=method,
                           params=dict(cmd=command, version=version),
                           id=id_num,)
            payload_list.append(payload)
            id_num += 1
        print(payload_list)
        return payload_list

    def send_request(self, commands, method='cli', timeout=30):
        """
        Send a HTTP/HTTPS request containing the JSON-RPC payload, headers, and username/password.

        method = cli for structured data response
        method = cli_ascii for a string response (still in JSON-RPC dict, but in 'msg' key)
        """
        timeout = int(timeout)
        payload_list = self._build_payload(commands, method)
        response = requests.post(self.url,
                                 timeout=timeout,
                                 data=json.dumps(payload_list),
                                 headers=self.headers,
                                 auth=HTTPBasicAuth(self.username, self.password),
                                 verify=self.verify)
        response_list = json.loads(response.text)

        if isinstance(response_list, dict):
            response_list = [response_list]

        # Add the 'command' that was executed to the response dictionary
        for i, response_dict in enumerate(response_list):
            response_dict['command'] = commands[i]
        return response_list
