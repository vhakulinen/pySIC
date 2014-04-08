import unittest
# import xml.etree.ElementTree as ET
import json
from server import pySIMServer


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.server = pySIMServer()

    def test_all(self):
        all_dict = self.server.get_all()

        keys = all_dict.keys()
        for i in ['sys', 'disks', 'mem', 'cpu', 'netio']:
            self.assertNotEqual(None, i in keys,
                    "Element %s not found." % i)

    def test_sys_info(self):
        # TODO: Improve system info
        sys_dict = self.server.sys_info()

        keys = sys_dict.keys()
        for i in ['hostname', 'uname-a']:
            self.assertEqual(True, i in keys,
                    "Element %s not found." % i)

    def test_mem_info(self):
        # mem_info() returns dict
        mem_dict = self.server.mem_info()

        # Let's save the keys so that we dont have to call that function
        # every time we loop
        keys = mem_dict.keys()
        for i in ['used', 'free', 'available', 'total']:
            self.assertEqual(True, i in keys,
                    "%s not found in mem_dict" % i)

            # Same goes here
            ekeys = mem_dict[i].keys()
            for j in ['bytes', 'human']:
                self.assertEqual(True, j in ekeys,
                        "%s not found from %s" % (j, i))

        self.assertEqual(True, 'percent' in keys,
                'Percent not found in mem_dict')

    def test_netio_info(self):
        net_list = self.server.netio_info()

        self.assertNotEqual(0, len(net_list))

        for iface in net_list:
            for i in ['total', 'per-sec']:
                self.assertEqual(True, i in iface)
                
                entry = iface[i]
                for io in ['sent', 'recv']:
                    self.assertEqual(True, io in entry)

                    for var in ['human', 'bytes']:
                        self.assertEqual(True, var in entry[io])

            self.assertEqual(True, 'name' in iface)

    def test_cpu_info(self):
        # TODO: Improve cpu info
        cpu_list = self.server.cpu_info()

        for cpu in cpu_list:
            #keys = cpu_dict[cpu].keys()
            self.assertEqual(True, 'percent' in cpu)
            self.assertEqual(True, 'index' in cpu)

    def test_disk_info(self):
        disk_list = self.server.disk_info()

        self.assertNotEqual(0, len(disk_list))

        for partition in disk_list:
            #keys = disk_dict[partition].keys()
            for i in ['device', 'mountpoint', 'fstype', 'opts', 'usage', 'index']:
                self.assertEqual(True, i in partition,
                        "Element %s not found." % i)

            skeys = partition['usage'].keys()
            for i in ['free', 'used', 'total', 'percent']:
                self.assertEqual(True, i in skeys, "Element %s not found.")


if __name__ == '__main__':
    unittest.main()
