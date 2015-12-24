# !/usr/bin/python env
# -*- coding: utf-8 -*-
import hexdump
from wifi_config import *


config = set_time()
config_type = 2

port = 8081
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', port))
print "waitting on port:", port
while True:
    data, addr = s.recvfrom(4096)
    result = hexdump.dump(data)
    # print result.split(' ')
    print "Received:", result, "from", addr
    print result[:8].split(' ')
    if result[:8] == "3C 3C 3C":
        msg = Frame(config_type, config).frame
        s.sendto(msg, addr)
	print "config device ........"
