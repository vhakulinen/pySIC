import commands
#import xml.etree.ElementTree as ET
import json
import signal
import sys
import time

# For getting local ip
import socket

# Third party
import Pyro4
import psutil


def sizeof_fmt(num):
    """ bytes -> human readable string """
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


class pySIMServer(object):
    def get_all_text(self):
        return json.dumps(self.get_all())

    def mem_info_text(self):
        return json.dumps(self.mem_info())

    def sys_info_text(self):
        return json.dumps(self.sys_info())

    def disk_info_text(self):
        return json.dumps(self.disk_info())

    def cpu_info_text(self):
        return json.dumps(self.cpu_info())

    def get_all(self):
        all_dict = { }
        all_dict.update({'sys': self.sys_info()})
        all_dict.update({'mem': self.mem_info()})
        all_dict.update({'cpu': self.cpu_info()})
        all_dict.update({'disks': self.disk_info()})
        all_dict.update({'netio': self.netio_info()})

        return all_dict

    def sys_info(self):
        uname = commands.getoutput('uname -a')
        hostname = commands.getoutput('echo $HOSTNAME')
        if hostname == '':
            hostname = commands.getoutput('hostname')

        sys_dict = { }

        sys_dict.update({'uname-a': uname})
        sys_dict.update({'hostname': hostname})

        return sys_dict

    def netio_info(self):
        pernic_counters_before = psutil.net_io_counters(pernic=True)
        time.sleep(1)
        pernic_counters_after = psutil.net_io_counters(pernic=True)
        net_list = [ ]

        for iface in pernic_counters_before:
            after = pernic_counters_after[iface]
            before = pernic_counters_before[iface]
            net_list.append({ 
                'name': iface,
                'total': {
                    'sent': {
                        'human': sizeof_fmt(after.bytes_sent),
                        'bytes': after.bytes_sent
                        },
                    'recv': {
                        'human': sizeof_fmt(after.bytes_recv),
                        'bytes': after.bytes_recv
                        }
                    },
                'per-sec': {
                    'sent': {
                        'human': sizeof_fmt((after.bytes_sent - before.bytes_sent)),
                        'bytes': (before.bytes_sent - after.bytes_sent)
                        },
                    'recv': {
                        'human': sizeof_fmt((after.bytes_recv - before.bytes_recv)),
                        'bytes': (before.bytes_recv - after.bytes_recv)
                        }
                    },
                'name': iface
            })

        return net_list

    def disk_info(self):
        partition_data = psutil.disk_partitions()

        disks_list = [ ]

        for i, partition in enumerate(partition_data):
            partition_dict = { }

            partition_dict.update({'index': str(i)})

            for entry in ['device', 'mountpoint', 'fstype', 'opts']:
                partition_dict.update({entry: getattr(partition, entry)})

            usage_data = psutil.disk_usage(partition.mountpoint)
            usage_dict = { }

            for entry in ['free', 'used', 'total']:
                usage_dict.update({entry: sizeof_fmt(getattr(usage_data, entry))})

            usage_dict.update({'percent': str(usage_data.percent)})
            partition_dict.update({'usage': usage_dict})
            disks_list.append(partition_dict)

        return disks_list

    def cpu_info(self):
        # TODO: Improve cpu info
        cpu_percent = psutil.cpu_percent(percpu=True)

        cpu_list = [ ]

        for i, x in enumerate(cpu_percent):
            cpu = { }
            cpu.update({'percent': str(x)})
            cpu.update({'index': str(i)})
            cpu_list.append(cpu)

        return cpu_list

    def mem_info(self):
        mem_data = psutil.virtual_memory()

        mem_dict = { }

        for entry in ['total', 'available', 'used', 'free']:
            # Let's create temp dict for entry and add data to it
            entry_dict = {'bytes': str(getattr(mem_data, entry))}
            entry_dict.update({'human': sizeof_fmt(getattr(mem_data, entry))})
            # Then lets add that dict to our main dict under current entry
            mem_dict.update({entry: entry_dict})

        # Let's not froget the percent
        mem_dict.update({'percent': str(mem_data.percent)})

        return mem_dict


def signal_handler(signal, frame):
    print "Received SIGINT. Exiting."
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    # To get the local ip
    s = socket.socket()
    s.connect(('google.com', 80))
    local_ip = s.getsockname()[0]
    s.close()

    serv = pySIMServer()

    daemon = Pyro4.Daemon(host=local_ip)
    ns = Pyro4.locateNS()
    uri = daemon.register(serv)
    ns.register('pysim.server:%s' % local_ip, uri)
    print "Ready. Press ^C to quit."
    daemon.requestLoop()
