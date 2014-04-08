pySIC
=====

pySIC - Python System Information Center

Requirements
----------
* Pyro4
* psutil
* dicttoxml (for simpleAdmin.py)

Usage
=====

Pyro4
-----
First off, make sure you have your Pyro4 nameserver running.
Do this by running following command:

    python -m Pyro4.naming -n <local_ip>

server.py
---------
Run server.py on machines where you wish to gather information.
This currently provides information about CPU, RAM, disks and networking.

simpleAdmin.py
--------------
This is simple admin script to gather information from all server defined.
`servers` list must contain server IPs where server.py is running and
`nameserver` must contain IP and PORT of server where Pyro's nameserver is running
