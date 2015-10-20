#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
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
        print values
        cur.executemany(sql, values)
        conn.commit()
        cur.close()
        conn.close()
    except:
        print "insert data failed!"
