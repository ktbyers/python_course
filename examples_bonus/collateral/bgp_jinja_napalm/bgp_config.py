from __future__ import print_function, unicode_literals
from jinja2 import FileSystemLoader, StrictUndefined
from jinja2.environment import Environment

from napalm import get_network_driver
from my_devices import arista1, arista2, arista3, arista4

env = Environment(undefined=StrictUndefined)
env.loader = FileSystemLoader('.')


def gen_bgp_peers(bgp_peer_list):
    bgp_return = []
    for peer in bgp_peer_list:
        peer_dict = {
            'peer_ip': peer['local_ip'],
            'peer_as': peer['local_as']
        }
        bgp_return.append(peer_dict)

    return bgp_return


def main():
    sw1 = {'local_as': '100', 'local_ip': '10.220.88.28'}
    sw2 = {'local_as': '101', 'local_ip': '10.220.88.29'}
    sw3 = {'local_as': '102', 'local_ip': '10.220.88.30'}
    sw4 = {'local_as': '103', 'local_ip': '10.220.88.31'}

    sw1_peers = gen_bgp_peers([sw2, sw3, sw4])
    sw2_peers = gen_bgp_peers([sw1, sw3, sw4])
    sw3_peers = gen_bgp_peers([sw1, sw2, sw4])
    sw4_peers = gen_bgp_peers([sw1, sw2, sw3])

    sw1['bgp_peers'] = sw1_peers
    sw2['bgp_peers'] = sw2_peers
    sw3['bgp_peers'] = sw3_peers
    sw4['bgp_peers'] = sw4_peers

    sw1['napalm_info'] = arista1
    sw2['napalm_info'] = arista2
    sw3['napalm_info'] = arista3
    sw4['napalm_info'] = arista4

    for bgp_vars in [sw1, sw2, sw3, sw4]:
        print()
        # print(switch_name)
        print('-' * 30)
        template_file = 'bgp.j2'
        template = env.get_template(template_file)
        bgp_config = 'no router bgp {}\n'.format(bgp_vars['local_as'])
        bgp_config += template.render(bgp_vars)

        # Establish a NAPALM connection
        napalm_info = bgp_vars['napalm_info']
        device_type = napalm_info.pop('device_type')
        driver = get_network_driver(device_type)
        device = driver(**napalm_info)
        print()
        print(">>>NAPALM Device open")
        device.open()
        print(device.get_facts())

        # Use a merge operation to push the config to the device
        print()
        print(">>>Load config change")
        device.load_merge_candidate(config=bgp_config)

        # Generate a diff
        print(device.compare_config())
        input("Hit any key to continue: ")

        # Commit the config
        device.commit_config()


if __name__ == "__main__":
    main()
