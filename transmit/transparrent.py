#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import select

host = '127.0.0.1'
port = 8088
s_up = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_down = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s_up.bind((' ', 8081))
s_down.bind((' ', 8088))
s_up.setblocking(0)
s_down.setblocking(0)
while True:
    up_ready = select.select([s_up], [], [], 2)
    if up_ready[0]:
        up_data, up_addr = s_up.recvfrom(4096)
        s_up.sendto(up_data, (host, port))
    else:
        print "waitting for up data"
    down_ready = select.select([s_down], [], [], 2)
    if down_ready[0]:
        down_data, down_addr = s_down.recvfrom(4096)
        s_down.sendto(down_data, up_addr)
    else:
        print "waitting for down_data"
