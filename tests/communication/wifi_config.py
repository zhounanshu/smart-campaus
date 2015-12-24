#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import socket
import struct

time_start = "2000-01-01 00:00:00"
base_time = datetime.datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S")


def get_data(frame, frame_lens, order):
    count = 0
    i = 0
    for value in frame_lens:
        if i == order:
            start = count
            end = count + value
            break
        count += value
        i += 1
    result = frame[start: end]
    return result


def toString(values):
    temp = ''
    for value in values:
        if value is not "00":
            temp += value.decode('hex')
    return temp


def toInt(values):
    i = len(values)
    temp = 0
    for value in values:
        i -= 1
        weight = 256 ** i
        temp += int(value, 16) * weight
    return temp

def toFloat(values):
    temp = ''
    if len(values) < 4:
	values = ['00' for i in range(4-len(values))] + values
    for value in values:
        temp += value
    return str(struct.unpack('f', temp.decode('hex'))[0])

def toIp(values):
    ip = ''
    for temp in values:
        ip += str(int(temp, 16))
        ip += '.'
    return ip[: -1]

def toTime(value):
    temp = base_time + datetime.timedelta(seconds=toInt(value))
    return temp.strftime("%Y-%m-%d %H:%M:%S")

def checkCRC(message):
    u8MSBInfo = 0x00
    u16CrcData = 0xffff
    for data in message:
        u16CrcData = u16CrcData ^ int(data, 16)
        for i in range(8):
            u8MSBInfo = u16CrcData & 0x0001
            u16CrcData = u16CrcData >> 1
            if u8MSBInfo != 0:
                u16CrcData = u16CrcData ^ 0xA001
    length = len(str(format(u16CrcData, 'x')))
    result = []
    if length == 1:
        result.append('0' + str(format(u16CrcData, 'x')))
    else:
        result = [str(format(u16CrcData, 'x'))[2 * i: 2 * i + 2]
                  for i in range(length / 2)]
    if len(result) < 2:
        result = ['00'] + result  
    return result

wifi_config_frame = [2, 4, 4, 4, 2, 1, 1, 1, 4, 4, 4, 4, 4, 2, 2, 4, 2, 40, 4,
                     2, 40, 32, 1, 32, 1, 32, 1, 32, 1, 1, 4, 4, 4, 4, 4, 4, 4,
                     4, 4, 4, 4, 4, 4]
config_answer_frame = [2, 4, 1]
wdsdhwwd_frame = [2, 4, 4, 4, 1, 1, 1, 2, 2, 2, 2, 4, 2, 4, 4, 4, 4]
wifi_data_answer_frame = [2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                           4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

wifi_config = ['00', '04', '00', '00', '21', '99', '1D', 'B3', '95', '8B', '00', '00', '04', '76', '00', '01', '01', '01', '01', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '05', '00', '01', 'C0', 'A8', '01', '78', '1F', '91', '31', '2E', '31', '2E', '31', '2E', '31', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', 'C0', 'A8', '00', '0A', '1F', '93', '32', '2E', '32', '2E', '32', '2E', '32', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '4C', '61', '62', '33', '30', '35', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00',
               '00', '00', '00', '00', '00', '00', '00', '0C', '6E', '65', '74', '63', '65', '6E', '74', '65', '72', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '6C', '6D', '73', '6B', '6A', '63', '78', '74', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '0D', '35', '38', '36', '30', '37', '37', '38', '30', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '03', '00', '00', '00', '01', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A', '0A']

# crc = ['BC', 'B1']
# device_time = get_data(wifi_config, wifi_config_frame, 2)
# device_id = get_data(wifi_config, wifi_config_frame, 3)
device_ip = get_data(wifi_config, wifi_config_frame, 8)
# fre = get_data(wifi_config, wifi_config_frame, 13)
# send_fre = get_data(wifi_config, wifi_config_frame, 14)
host_ip = get_data(wifi_config, wifi_config_frame, 15)
# ssid = get_data(wifi_config, wifi_config_frame, 21)
# passwd = get_data(wifi_config, wifi_config_frame, 23)
# check CRC
# print checkCRC(wifi_config)
# print toInt(crc)
# device time
# d = base_time + datetime.timedelta(seconds=toInt(device_time))
# print d

# t = ['1D' 'B2' '13' 'DB']
# print (base_time + datetime.timedelta(seconds=toInt(t)))
# device id
# print device_id
# print toInt(device_id)
# device ssid and password
# print ssid + passwd
# print toString(ssid), toString(passwd)

# frequency min
# print toInt(fre), toInt(send_fre)

# print host_ip
# print host_ip
print toIp(host_ip), toIp(device_ip)

# CONFIG_FRAME


def int_to_hex(para, length):
    result = []
    temp = []
    data = format(para, 'x')
    if len(str(data)) == 1:
        result.append('0' + str(data))
    else:
        for i in range(len(str(data)) / 2):
            result.append(data[2 * i: 2 * i + 2])
    distance = length - len(result)
    if distance != 0:
        temp = ['00' for n in range(distance)]
    return temp + result


def str_to_hex(para, length):
    result = []
    temp = []
    data = para.encode('hex')
    result = [data[2 * i: 2 * i + 2] for i in range(len(data) / 2)]
    distance = length - len(result)
    if distance != 0:
        temp = ['00' for i in range(distance)]
    return result + temp


def set_time():
    config_type = ['00', '02']
    delta_time = datetime.datetime.now() - base_time
    delta_seconds = delta_time.seconds + delta_time.days * 24 * 3600
    return config_type + int_to_hex(delta_seconds, 4)


# set frequency mins
def set_frequency(mins):
    config_type = ['00', '09']
    return config_type + int_to_hex(mins, 2)


# set send intervals
def set_intervals(counts):
    config_type = ['00', '0A']
    return config_type + int_to_hex(counts, 2)


# set sever ip and port
def set_host(host, port, flag):
    if flag == 1:
        config_host_type = ['00', '0B']
        config_port_type = ['00', '0C']
    elif flag == 2:
        config_host_type = ['00', '0E']
        config_port_type = ['00', '0F']
    else:
        print "you are setting wrong flag!"
    host_list = []
    elements = host.split('.')
    for element in elements:
        host_list += int_to_hex(int(element), 1)
    port_list = int_to_hex(port, 2)
    addr_host = config_host_type + host_list
    addr_port = config_port_type + port_list
    return addr_host + addr_port


# set ssid and password
def set_wifi(ssid, passwd, flag):
    if flag == 1:
        config_ssid_type = ['01', '01']
        config_pwd_type = ['01', '03']
    elif flag == 2:
        config_ssid_type = ['01', '04']
        config_pwd_type = ['01', '06']
    else:
        print "with ssid: you are setting wrong flag!"
    ssid_config = config_ssid_type + str_to_hex(ssid, 32)
    passwd_config = config_pwd_type + str_to_hex(passwd, 32)
    return ssid_config + passwd_config

# print set_time()
# print set_frequency(15)
# print set_host('192.168.1.120', 8081, 1)

# config answer frame


def configFaild(frame):
    flag = True
    device_id = toInt(frame[2: 6])
    if toInt(frame[6]) == 0:
        flag = False
        print "the device", device_id, "set failed!"
        return flag


config_fra = ['00', '02', '00', '01', '00', '00',
              '04', '6C', '00', '02', '1D', 'B2', '13' 'DB']


class Frame(object):

    def __init__(self, frame_type, arg):
        self.frame_type = int_to_hex(frame_type, 2)
        self.arg = arg
        self.start = ['3C', '3C', '3C']
        self.end = ['3E', '3E', '3E']
        self.temp = ''
        self.crc = checkCRC(self.frame_type + self.arg)
        temp = self.start + self.frame_type + self.arg + self.crc + self.end
        frame = ''
        for value in temp:
            frame += value
        self.temp = frame
        self.frame = frame.decode('hex')

    def get_frame(self):
        return self.frame

# config = ['00','01','00','00','04','6C','00','02','1D','B2','13','DB']
# print Frame(2, config, ('192.168.1.104', 5000)).send_frame()
