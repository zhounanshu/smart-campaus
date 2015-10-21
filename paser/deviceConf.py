#!/usr/bin/python env
# -*- coding: utf-8 -*-
import hexdump
import socket
from wifi_config import *
import select

config = set_time() + set_host('127.0.0.1', 8081, 1) + \
    set_wifi('shisu', '', 2)
config_type = 2

port = 8081
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', port))
s.setblocking(0)
print "waitting on port:", port

while True:
    ready = select.select([s], [], [], 2)
    if ready[0]:
        data, addr = s.recvfrom(4096)
        result = hexdump.dump(data)
        # print "Received:", result, "from", addr
        if result[:8] == "3C 3C 3C":
            raw_data = result.split(' ')
            frame_head = raw_data[: 3]
            frame_content = raw_data[3: -5]
            crc_check = raw_data[-5: -3]
            frame_end = raw_data[-3:]
            frame_type = toInt(frame_content[:2])
            if frame_type == 3:
                if toInt(checkCRC(frame_content)) != toInt(crc_check):
                    print checkCRC(frame_content), crc_check
                    print "crc check error!"
                    continue
                else:
                    if not configFailed(frame_content):
                        print "config successful........"
            elif frame_type == 4:
                if toInt(checkCRC(frame_content)) != toInt(crc_check):
                    print checkCRC(frame_content), crc_check
                    print "crc check error!"
                    continue
                else:
                    frequency = toInt(
                        get_data(frame_content, wifi_config_frame, 13))
                    jiange = toInt(
                        get_data(frame_content, wifi_config_frame, 14))
                    ssid1 = toString(
                        get_data(frame_content, wifi_config_frame, 21))
                    passwd = toString(
                        get_data(frame_content, wifi_config_frame, 23))
                    device_id = toInt(
                        get_data(frame_content, wifi_config_frame, 3))
                    print ssid1, passwd, frequency, jiange
                    msg = Frame(config_type, config).frame
                    print Frame(config_type, config).temp
                    s.sendto(msg, addr)
                    print "config device ........"
            elif frame_type == 100:
                print 'receview sensor data......'
    else:
        print 'i am waitting......'
