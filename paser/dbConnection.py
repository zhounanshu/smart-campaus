#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import urllib2
import urllib
import json
from confLoad import confLoader
from confLoad import *

TEMPERATURE = 1
HUMIDITY = 2
NOISE = 3
PM2_5 = 4


def Post(args):
    config = confLoader()
    try:
        conn = MySQLdb.connect(host=config.get_host(),
                               port=config.get_port(),
                               user=config.get_user(),
                               passwd=config.get_passwd(),
                               db=config.get_db(),
                               charset='utf8')
        cur = conn.cursor()
        sql = 'insert into sensor_data(device_id, sensor_id, value,\
                datetime, ele_quantity, voltage, \
                device_temp) values (%s, %s,%s, %s, %s, %s, %s)'
        values = []
        for arg in args:
            datetime = arg["time"]
            temperature = arg["temperature"]
            humidity = arg['humidity']
            noise = arg['noise']
            pm2_5 = arg['pm2_5']
            device_id = arg['device_id']
            voltage = arg['voltage']
            ele_quantity = arg['ele_quantity']
            device_temp = arg['device_temp']
            values.append(
                (device_id, TEMPERATURE, temperature,
                    datetime, ele_quantity, voltage, device_temp))
            values.append(
                (device_id, HUMIDITY, humidity, datetime,
                 ele_quantity, voltage, device_temp))
            values.append(
                (device_id, NOISE, noise, datetime,
                    ele_quantity, voltage, device_temp))
            values.append(
                (device_id, PM2_5, pm2_5, datetime,
                 ele_quantity, voltage, device_temp))
        cur.executemany(sql, values)
        conn.commit()
        cur.close()
        conn.close()
    except:
        print "insert data failed!"


def postData(arg, sensorType):
    config = confLoader()
    url = config.get_url()
    temp = {}
    temp['datetime'] = arg["time"]
    temp['device_id'] = arg['device_id']
    temp['voltage'] = arg['voltage']
    temp['ele_quantity'] = arg['ele_quantity']
    temp['device_temp'] = arg['device_temp']
    if sensorType == TEMPERATURE:
        temp['value'] = arg['temperature']
        temp['sensor_id'] = TEMPERATURE
    if sensorType == HUMIDITY:
        temp['value'] = arg['humidity']
        temp['sensor_id'] = HUMIDITY
    if sensorType == PM2_5:
        temp['value'] = arg['pm2_5']
        temp['sensor_id'] = PM2_5
    if sensorType == NOISE:
        temp['value'] = arg['noise']
        temp['sensor_id'] = NOISE
    req = urllib2.Request(url, json.dumps(temp))
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req)
    return True


args = [{'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '-inf', 'temperature': '32.0545425415', 'device_temp': '33.75', 'humidity': '42.583984375', 'voltage': 41, 'time': '2015-10-25 11:02:58', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '72.584197998', 'temperature': '32.0759963989', 'device_temp': '34.0', 'humidity': '42.6221313477', 'voltage': 41, 'time': '2015-10-25 11:08:22', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '86.0195236206', 'temperature': '32.1403427124', 'device_temp': '34.0', 'humidity': '42.6831665039', 'voltage': 41, 'time': '2015-10-25 11:13:45', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '75.3794403076', 'temperature': '32.1832504272', 'device_temp': '34.25', 'humidity': '42.6145019531', 'voltage': 41, 'time': '2015-10-25 11:19:09', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '44.8583068848', 'temperature': '32.215423584', 'device_temp': '34.0', 'humidity': '42.5458374023', 'voltage': 41, 'time': '2015-10-25 11:24:32', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '75.9075164795', 'temperature': '32.2797698975', 'device_temp': '34.0', 'humidity': '42.2406616211', 'voltage': 41, 'time': '2015-10-25 11:29:56', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 93, 'noise': '86.9784851074', 'temperature': '32.1510696411', 'device_temp': '32.75', 'humidity': '42.3093261719', 'voltage': 41, 'time': '2015-10-25 11:35:19', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '86.5239181519', 'temperature': '32.0545425415', 'device_temp': '32.5', 'humidity': '42.2788085938', 'voltage': 41, 'time': '2015-10-25 11:40:43', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '87.3495483398', 'temperature': '31.990196228', 'device_temp': '32.25', 'humidity': '42.3856201172', 'voltage': 41, 'time': '2015-10-25 11:46:06', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '87.3495483398', 'temperature': '31.9794692993', 'device_temp': '32.75', 'humidity': '42.454284668', 'voltage': 41, 'time': '2015-10-25 11:51:30', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '81.0996017456', 'temperature': '31.990196228', 'device_temp': '33.0', 'humidity': '42.4161376953', 'voltage': 41, 'time': '2015-10-25 11:56:53', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '52.8647842407', 'temperature': '32.0223693848', 'device_temp': '33.25', 'humidity': '42.3856201172', 'voltage': 41, 'time': '2015-10-25 12:02:17', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '82.4123535156', 'temperature': '32.0545425415', 'device_temp': '33.5', 'humidity': '42.1109619141', 'voltage': 41, 'time': '2015-10-25 12:07:40', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '81.7910308838', 'temperature': '32.097442627', 'device_temp': '33.75', 'humidity': '41.7752685547', 'voltage': 41, 'time': '2015-10-25 12:13:04', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '20.2593383789', 'temperature': '32.1617965698', 'device_temp': '34.0', 'humidity': '41.5616455078', 'voltage': 41, 'time': '2015-10-25 12:18:27', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '52.6575279236', 'temperature': '32.2046966553', 'device_temp': '34.25', 'humidity': '41.2564697266', 'voltage': 41, 'time': '2015-10-25 12:23:51', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '83.5555114746', 'temperature': '32.2583236694', 'device_temp': '34.25', 'humidity': '40.9512939453', 'voltage': 41, 'time': '2015-10-25 12:29:14', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '33.5889205933', 'temperature': '32.3333969116', 'device_temp': '34.5', 'humidity': '40.7300415039', 'voltage': 41, 'time': '2015-10-25 12:34:38', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '57.2863731384', 'temperature': '32.3870239258', 'device_temp': '34.75', 'humidity': '40.4630126953', 'voltage': 41, 'time': '2015-10-25 12:40:01', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 93, 'noise': '79.6946029663', 'temperature': '32.2583236694', 'device_temp': '32.75', 'humidity': '40.6461181641', 'voltage': 41, 'time': '2015-10-25 12:45:25', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '86.4471435547', 'temperature': '32.1725234985', 'device_temp': '32.5', 'humidity': '40.6079711914', 'voltage': 41, 'time': '2015-10-25 12:50:48', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '81.1497955322', 'temperature': '32.097442627', 'device_temp': '32.5', 'humidity': '40.5850830078', 'voltage': 41, 'time': '2015-10-25 12:56:12', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '81.6448669434', 'temperature': '32.0759963989', 'device_temp': '32.75', 'humidity': '40.5545654297', 'voltage': 41, 'time': '2015-10-25 13:01:35', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '0.288772583008', 'temperature': '32.0867233276', 'device_temp': '33.0', 'humidity': '40.4477539062', 'voltage': 41, 'time': '2015-10-25 13:06:59', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '67.3369140625', 'temperature': '32.1081695557', 'device_temp': '33.25', 'humidity': '40.272277832', 'voltage': 41, 'time': '2015-10-25 13:12:23', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '-inf', 'temperature': '32.1403427124', 'device_temp': '33.5', 'humidity': '40.0662841797', 'voltage': 41, 'time': '2015-10-25 13:17:46', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '85.5423660278', 'temperature': '32.1725234985', 'device_temp': '33.75', 'humidity': '39.8984375', 'voltage': 41, 'time': '2015-10-25 13:23:10', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '83.5555114746', 'temperature': '32.2046966553', 'device_temp': '33.75', 'humidity': '39.7611083984', 'voltage': 41, 'time': '2015-10-25 13:28:33', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '62.4954795837', 'temperature': '32.2475967407', 'device_temp': '34.0', 'humidity': '39.5627441406', 'voltage': 41, 'time': '2015-10-25 13:33:56', 'device_id': 1162}, {'pm2_5': '10.0', 'ele_quantity': 94, 'noise': '86.4471435547', 'temperature': '32.2904968262', 'device_temp': '34.25', 'humidity': '39.4788208008', 'voltage': 41, 'time': '2015-10-25 13:39:20', 'device_id': 1162}]

for arg in args:
    postData(arg, 1)
    postData(arg, 2)
    postData(arg, 3)
    postData(arg, 4)
