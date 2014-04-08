import Pyro4
import time
import xml.etree.ElementTree as ET
import dicttoxml
import json

servers = [ '127.0.0.1' ]
nameserver = ('127.0.0.1', 9090)

def main():
    ns = Pyro4.locateNS(host=nameserver[0], port=nameserver[1])
    while True:
        data = ET.Element('root')
        for server in servers:
            uri = ns.lookup('pysim.server:%s' % server)
            c = Pyro4.Proxy(uri)
            json_data = c.get_all()
            xml_data = dicttoxml.convert(json_data, 0)
            xml_data = ET.fromstring('<data>' + xml_data + '</data>')
            data.append(xml_data)
        f = open('data.xml', 'w')
        f.write('<?xml version="1.0"?>')
        f.write('<?xml-stylesheet href="data.xsl" type="text/xsl"?>')

        f.write(ET.tostring(data))
        f.close()
        time.sleep(3)

if __name__ == '__main__':
    main()
