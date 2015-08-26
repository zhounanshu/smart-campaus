#!usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.restful import Api
from main.views import *


def create_app(cnf):
    app = Flask(__name__)
    app.config.from_object(cnf)
    db.init_app(app)
    api = Api(app)
    api.add_resource(UserList, '/user', '/user/')
    api.add_resource(UserResource, '/user/<user_id>')
    api.add_resource(Login, '/login', '/login/')
    api.add_resource(BuildingList, '/building', '/building/')
    api.add_resource(BuildingResource, '/building/<building_id>')
    api.add_resource(FloorList, '/floor', '/floor/')
    api.add_resource(FloorResource, '/floor/<floor_id>')
    api.add_resource(RoomList, '/room', '/room/')
    api.add_resource(RoomResource, '/room/<room_id>')
    api.add_resource(DeviceList, '/device', '/device/')
    api.add_resource(DeviceResource, '/device/<device_id>')
    api.add_resource(dList, '/data', '/data/')
    api.add_resource(DataResource, '/data/<data_id>')
    api.add_resource(sensorList, '/sensor', '/sensor/')
    api.add_resource(sensorResource, '/sensor/<sensor_id>')
    api.add_resource(locationResource, '/location/<uuid>')
    api.add_resource(locationList, '/location', '/location/')
    api.add_resource(dataSensor, '/type/data', '/type/data/')
    api.add_resource(dataList, '/all/data', '/all/data/')
    api.add_resource(locationInfor, '/get/location', '/get/location/')

    return app
