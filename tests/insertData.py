#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import random
import datetime
import requests
import json
import uuid


def random_str(strLen):
    a = list(string.ascii_lowercase)
    random.shuffle(a)
    return ''.join(a[: strLen])


def random_psword(pslen):
    letterList = list(string.ascii_letters)
    numList = list(str(xrange(10)))
    a = letterList + numList
    random.shuffle(a)
    return ''.join(a[: pslen])


def random_date(startYear, endYear):
    year = random.randint(startYear, endYear)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    date = datetime(year, month, day)
    birth_date = datetime.strftime(date, "%Y-%m-%d")
    return birth_date


def loaction():
    latitude = str(random.uniform(120.51, 122.12))[:7]
    longitude = str(random.uniform(30.40, 31.53))[:6]
    return (latitude, longitude)


def postData(table, dJson):
    url = "http://127.0.0.1:5000/api/v1.0/" + table
    requests.post(url, data=json.dumps(dJson),
                  headers={'content-type': 'application/json'})


def building():
    buildList = ["图书馆", "一教学楼", "二教学楼",
                 "三教学楼", "四教学楼", "五教学楼",
                 "六教学楼"]
    return random.choice(buildList)


def floor():
    floorList = ['1', '2', '3', '4', '5', '6']
    return random.choice(floorList)


def room():
    roomList = ['001', '002', '003', '004', '005', '006']
    return random.choice(roomList)


def id():
    deviceId = str(uuid.uuid1())
    f = open('./deviceId.txt', 'a')
    toWrite = deviceId + '\n'
    f.writelines(toWrite)
    f.close()
    return deviceId


def sensorName():
    sensorList = [('sht21', 'temperature'),
                  ('sht21', 'humidity'), ('seeed', 'noise'),
                  ('GE', 'pm2.5'), ('GE', 'pm10')]
    return random.choice(sensorList)

# # inser table user
# for i in range(20):
#     user = {}
#     user['username'] = random_str(4)
#     user['password'] = random_psword(6)
#     user['email'] = random_str(6) + "@" + "163.com"
#     postData('user', user)

# insert table building

# buildList = ["一教学楼", "二教学楼",
#              "三教学楼", "四教学楼", "五教学楼",
#              "六教学楼"]
# for name in buildList:
#     build = {}
#     build['name'] = name
#     build['latitude'] = loaction()[1]
#     build['longitude'] = loaction()[0]
#     postData('building', build)

# # insert floor table
# for i in range(20):
#     floorInfor = {}
#     floorInfor['name'] = floor()
#     floorInfor['building_id'] = random.randint(1, 6)
#     postData('floor', floorInfor)

# # insert room table
# for i in range(20):
#     roomInfor = {}
#     roomInfor['name'] = room()
#     roomInfor['floor_id'] = random.randint(0, 20)
#     postData('room', roomInfor)

# # insert device table
# for i in range(20):
#     deviceInfor = {}
#     deviceInfor['room_id'] = random.randint(0, 20)
#     deviceInfor['uuid'] = id()
#     deviceInfor['name'] = 'AQM'
#     postData('device', deviceInfor)

# # insert sensor table
# sensorList = [('sht21', 'temperature'),
#               ('sht21', 'humidity'), ('seeed', 'noise'),
#               ('GE', 'pm2.5'), ('GE', 'pm10')]
# for sensor in sensorList:
#     sensorInfor = {}
#     sensorInfor['type'] = sensor[1]
#     sensorInfor['name'] = sensor[0]
#     f = open('sensor.txt', 'a')
#     # line = sensorInfor['uuid'] + '\n'
#     # f.writelines(line)
#     f.close()
#     postData('sensor', sensorInfor)

f_sensor = open('sensor.txt', 'r')
sensorId = []
for line in f_sensor:
    sensorId.append(line)
f_sensor.close()

f_deviceId = open('deviceId.txt', 'r')
deviceIdindex = 0
while True:
    deviceIdindex += 1
    line = f_deviceId.readline()
    if not line:
        break
    for i in range(1, 6):
        data = {}
        data['device_id'] = deviceIdindex
        data['value'] = random.randint(0, 100) + \
            float(str(random.random())[:3])
        data['sensor_id'] = i
        now = datetime.datetime.now()
        data['datetime'] = now.strftime("%Y-%m-%d %H:%M:%S")
        data['status'] = '1'
        print data
        postData('data', data)

