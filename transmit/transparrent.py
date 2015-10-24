#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket


localPort = 8081
remoteHost = '121.40.255.112'
remotePort = 8088


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', localPort))

knownClient = None
knownServer = (remoteHost, remotePort)
while True:
    data, addr = s.recvfrom(4096)
#        print "receiving:", hexdump.dump(data), "from", addr
    if knownClient is None:
        knownClient = addr
    if addr == knownClient:
#                print "sending:", hexdump.dump(data), "to", knownServer
        s.sendto(data, knownServer)
    else:
#                print "sending:", hexdump.dump(data), "to", knownClient
        s.sendto(data, knownClient)
