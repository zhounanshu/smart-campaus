#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hexdump
import socket
from wifi_config import *
import select

config = set_time()
config_type = 2

port = 8081
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind('', port)
s.setblocking(0)

