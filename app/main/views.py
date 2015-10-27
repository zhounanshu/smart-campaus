#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request
from flask.ext.restful import Resource, reqparse
from app.models import *


def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object. """
    json = {}
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        # json['fields'][col.name] = getattr(model, col.name)
        value = getattr(model, col.name)
        if isinstance(value, unicode):
            json[col.name] = getattr(model, col.name)
        else:
            json[col.name] = str(getattr(model, col.name))
    # return dumps([json])
    return json


def to_json_list(model_list):
    json_list = []
    for model in model_list:
        json_list.append(to_json(model))
    return json_list


class UserResource(Resource):

    def get(self, user_id):
        record = User.query.filter_by(id=user_id).first()
        return to_json(record), 200

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str)
        args = parser.parse_args(strict=True)
        record = User.query.filter_by(id=user_id).first()
        if record:
            record.passwd = args['password']
            db.session.commit()
            return {'status': 'updated'}, 201
        else:
            return {'status': 'user not exist'}, 404

    def delete(self, user_id):
        record = User.query.filter_by(id=user_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class UserList(Resource):

    def get(self):
        record_list = User.query.all()
        # return jsonify(json_list=[i.serialize for i in user_list]), 200
        # results = []
        # for idx in user_list:
        #     results.append(to_json(idx))
        return to_json_list(record_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args(strict=True)
        new_record = User(args['username'], args['password'], args['email'])
        db.session.add(new_record)
        result = db.session.commit()
        # new_user = User(username, password, email)
        # db.session.add(new_user)
        # result = db.session.commit()
        # return new_record.id, 201
        return result, 201


class Login(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        user = User.query.filter_by(name=args['username']).first()
        if user.verify_password(args['password']):
            return {'status': 'login successed'}, 200
        else:
            return {'status': 'login failed'}, 200


class BuildingResource(Resource):

    def get(self, building_id):
        record = Building.query.filter_by(id=building_id).first()
        if record:
            return to_json(record), 200
        return {"status": "the building is not exit!"}, 400

    def put(self, building_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode)
        args = parser.parse_args(strict=True)
        record = Building.query.filter_by(id=building_id).first()
        if record:
            try:
                record.name = args['name']
                db.session.commit()
                return {'status': 'updated'}, 201
            except:
                return {"status": "insert error!"}
        else:
            return {'status': 'building not exist!'}, 404

    def delete(self, building_id):
        record = Building.query.filter_by(id=building_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class BuildingList(Resource):

    def get(self):
        building_list = Building.query.all()
        # return jsonify(json_list=[i.serialize for i in user_list]), 200
        # results = []
        # for idx in user_list:
        #     results.append(to_json(idx))
        return to_json_list(building_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode)
        parser.add_argument('latitude', type=str)
        parser.add_argument('longitude', type=str)
        parser.add_argument('description', type=unicode)
        args = parser.parse_args(strict=True)
        new_record = Building(
            args['name'], args['latitude'],
            args['longitude'], args['description'])
        db.session.add(new_record)
        db.session.commit()
        # new_user = User(username, password, email)
        # db.session.add(new_user)
        # result = db.session.commit()
        return new_record.id, 201


class FloorResource(Resource):

    def get(self, floor_id):
        record = Floor.query.filter_by(id=floor_id).first()
        if record:
            return to_json(record), 200
        return {"status": "the floor is not exit"}, 400

    def put(self, floor_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode)
        args = parser.parse_args(strict=True)
        record = Floor.query.filter_by(id=floor_id).first()
        if record:
            record.name = args['name']
            db.session.commit()
            return {'status': 'updated'}, 201
        else:
            return {'status': 'floor not exist'}, 404

    def delete(self, floor_id):
        record = Floor.query.filter_by(id=floor_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class FloorList(Resource):

    def get(self):
        floor_list = Floor.query.all()
        # return jsonify(json_list=[i.serialize for i in user_list]), 200
        # results = []
        # for idx in user_list:
        #     results.append(to_json(idx))
        return to_json_list(floor_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('building_id', type=int)
        parser.add_argument('name', type=unicode)
        parser.add_argument('description', type=unicode)
        args = parser.parse_args(strict=True)
        new_record = Floor(
            args['building_id'], args['name'], args['description'])
        db.session.add(new_record)
        db.session.commit()
        return new_record.id, 201


class RoomResource(Resource):

    def get(self, room_id):
        record = Room.query.filter_by(id=room_id).first()
        if record:
            return to_json(record), 200
        return {"status": "the floor is not exit"}, 400

    def put(self, room_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        record = Room.query.filter_by(id=room_id).first()
        if record:
            record.name = args['name']
            db.session.commit()
            return {'status': 'updated'}, 201
        else:
            return {'status': 'room not exit'}, 404

    def delete(self, room_id):
        record = Room.query.filter_by(id=room_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class RoomList(Resource):

    def get(self):
        floor_list = Room.query.all()
        return to_json_list(floor_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('floor_id', type=int)
        parser.add_argument('name', type=unicode)
        parser.add_argument('description', type=unicode)
        args = parser.parse_args(strict=True)
        new_record = Room(
            args['floor_id'], args['name'], args['description'])
        db.session.add(new_record)
        db.session.commit()
        return new_record.id, 201


class DeviceResource(Resource):

    def get(self, device_id):
        record = Device.query.filter_by(id=device_id).first()
        if record is not None:
            return to_json(record), 200
        else:
            return {'status': 'device not exit'}

    def put(self, device_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode)
        args = parser.parse_args(strict=True)
        record = Device.query.filter_by(id=device_id).first()
        if record:
            record.name = args['name']
            db.session.commit()
            return {'status': 'updated'}, 201
        else:
            return {'status': 'device not exist!'}, 404

    def delete(self, device_id):
        record = Device.query.filter_by(id=device_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class DeviceList(Resource):

    def get(self):
        floor_list = Device.query.all()
        return to_json_list(floor_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('room_id', type=int)
        parser.add_argument('name', type=unicode)
        parser.add_argument('description', type=unicode)
        parser.add_argument('uuid', type=str)
        args = parser.parse_args(strict=True)
        new_record = Device(
            args['room_id'], args['name'],
            args['uuid'], args['description'])
        db.session.add(new_record)
        db.session.commit()
        return new_record.id, 201


class sensorResource(Resource):

    def get(self, sensor_id):
        record = Sensor.query.filter_by(id=sensor_id).first()
        if record is not None:
            return to_json(record), 200
        else:
            return {"status": "sensor not exit"}

    def put(self, sensor_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        record = Sensor.query.filter_by(id=sensor_id).first()
        if record:
            record.name = args['name']
            db.session.commit()
            return to_json(record), 201
        else:
            return {"status": "sensor not exit"}

    def delete(self, sensor_id):
        record = Sensor.query.filter_by(id=sensor_id).first()
        if record is not None:
            db.session.delete(record)
            db.session.commit()
            return {'status': 'deleted'}, 204
        else:
            return {"status": "sensor not exit"}


class sensorList(Resource):

    def get(self):
        floor_list = Sensor.query.all()
        return to_json_list(floor_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, location='json')
        parser.add_argument('name', type=unicode, location='json')
        # parser.add_argument('uuid', type=str, location='json')
        parser.add_argument('description', type=unicode, location='json')
        args = parser.parse_args(strict=True)
        new_record = Sensor(
            args['type'], args['name'], args['description'])
        db.session.add(new_record)
        db.session.commit()
        return new_record.id, 201


class DataResource(Resource):

    def get(self, data_id):
        record = SensorData.query.filter_by(id=data_id).first()
        # return jsonify(json_list=record), 200
        return to_json(record), 200

    def put(self, data_id):
        parser = reqparse.RequestParser()
        parser.add_argument('value', type=str)
        args = parser.parse_args(strict=True)
        record = SensorData.query.filter_by(id=data_id).first()
        if record:
            record.value = args['value']
            db.session.commit()
            return {"status": "updated"}, 201
        else:
            return {"status": "data not exit"}

    def delete(self, data_id):
        record = SensorData.query.filter_by(id=data_id).first()
        if not record:
            return {"status": "not exit"}
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class dList(Resource):

    def get(self):
        floor_list = SensorData.query.all()
        return to_json_list(floor_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('device_id', type=unicode)
        parser.add_argument('sensor_id', type=str)
        parser.add_argument('value', type=str)
        parser.add_argument("device_temp", type=str)
        parser.add_argument("voltage", type=str)
        parser.add_argument('ele_quantity', type=str)
        parser.add_argument('datetime', type=str)
        args = parser.parse_args(strict=True)
        new_record = SensorData(
            args['sensor_id'], args['device_id'], args['value'],
            args['datetime'], args['ele_quantity'], args['voltage'],
            args['device_temp'])
        db.session.add(new_record)
        db.session.commit()
        return new_record.id, 201


# add a new device


class locationList(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        parser.add_argument('build_name', type=unicode)
        parser.add_argument('floor_name', type=str)
        parser.add_argument('room_name', type=str)
        parser.add_argument('device_name', type=str)
        parser.add_argument('description', type=unicode)
        args = parser.parse_args(strict=True)
        buildInfor = Building.query.filter_by(
            name=args['build_name']).first()
        if buildInfor:
            floorInfor = Floor.query.filter_by(
                name=args['floor_name'],
                building_id=buildInfor.id).first()
            print args['room_name']
            print floorInfor.id
            if floorInfor:
                roomInfor = Room.query.filter_by(
                    name=args['room_name'],
                    floor_id=floorInfor.id).first()
                if roomInfor:
                    new_record = Device(
                        roomInfor.id, args['device_name'],
                        args['uuid'], args['description'])
                    db.session.add(new_record)
                    db.session.commit()
                return {"status": "insert successful"}, 201
            else:
                return {"error": "floor not exit"}, 400
        else:
            return {"error": "building not exit"}, 400

# lookup, update, delete a device


class locationResource(Resource):

    def get(self, uuid):
        record = Device.query.filter_by(uuid=uuid).first()
        if record:
            try:
                roomInfor = Room.query.filter_by(
                    id=record.room_id).first_or_404()
                floorInfor = Floor.query.filter_by(
                    id=roomInfor.floor_id).first_or_404()
                buildInfor = Building.query.filter_by(
                    id=floorInfor.building_id).first_or_404()
                deviceInfor = {}
                deviceInfor['floor_name'] = floorInfor.name
                deviceInfor['room_name'] = roomInfor.name
                deviceInfor['build_name'] = buildInfor.name
                return deviceInfor, 200
            except:
                return {"warning": "you may input error information,\
                please ask the Administrator"}
        else:
            return {"error": "device not exit"}, 400

    def put(self, uuid):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        args = parser.parse_args()
        record = Device.query.filter_by(uuid=uuid).first()
        if record:
            record.uuid = args['uuid']
            db.session.commit()
            return {"status": 'updated'}, 201
        else:
            return {"status": 'device not exit'}, 404

    def delete(self, uuid):

        record = Device.query.filter_by(uuid=uuid).first()
        if record:
            db.session.delete(record)
            db.session.commit()
            return {'status': 'deleted'}, 204
        else:
            return {'status': 'device not exit'}, 400


class dataSensor(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('build_name', type=unicode)
        parser.add_argument('floor_name', type=str)
        parser.add_argument('room_name', type=str)
        parser.add_argument('sensor_name', type=str)
        args = parser.parse_args(strict=True)
        buildInfor = Building.query.filter_by(
            name=args['build_name']).first_or_404()
        if buildInfor:
            floorInfor = Floor.query.filter_by(
                name=args['floor_name'],
                building_id=buildInfor.id).first_or_404()
            if floorInfor:
                roomInfor = Room.query.filter_by(
                    name=args['room_name'],
                    floor_id=floorInfor.id).first_or_404()
                if roomInfor:
                    deviceInfor = Device.query.filter_by(
                        room_id=roomInfor.id).first_or_404()
        sensorInfor = Sensor.query.filter_by(
            name=args['sensor_name']).first()
        if sensorInfor and deviceInfor:
            bufs = SensorData.query.filter_by(
                sensor_id=sensorInfor.id,
                device_id=deviceInfor.id
            ).order_by('datetime desc').limit(10)
            if bufs is not None:
                # return to_json_list(buf), 200
                results = []
                for buf in bufs:
                    result = {}
                    result["sensor_name"] = buf.sensor.name
                    result["value"] = buf.value
                    result["datetime"] = str(buf.datetime)
                    results.append(result)
                return results, 200
            else:
                return {"status": "no data"}
        else:
            return {"status": "no data"}


class dataList(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('build_name', type=unicode)
        parser.add_argument('floor_name', type=str)
        parser.add_argument('room_name', type=str)
        args = parser.parse_args(strict=True)
        buildInfor = Building.query.filter_by(
            name=args['build_name']).first_or_404()
        if buildInfor:
            floorInfor = Floor.query.filter_by(
                name=args['floor_name'],
                building_id=buildInfor.id).first_or_404()
            if floorInfor:
                roomInfor = Room.query.filter_by(
                    name=args['room_name'],
                    floor_id=floorInfor.id).first_or_404()
                if roomInfor:
                    deviceInfor = Device.query.filter_by(
                        room_id=roomInfor.id).first_or_404()
        if deviceInfor:
            results = SensorData.query.filter_by(
                device_id=deviceInfor.id
            ).order_by('datetime desc').limit(10)
            values = to_json_list(results)
            sensor_list = []
            for result in results:
                value = {}
                value["sensor"] = Sensor.query.filter_by(
                    id=result.sensor_id).first().name
                value["time"] = str(result.datetime)
                value["value"] = str(result.value)
                sensor_list.append(value)
        return sensor_list, 200


class locationInfor(Resource):

    def get(self):
        locaList = []
        rooms = Room.query.all()
        if rooms:
            for room in rooms:
                location = {}
                location['room_name'] = room.name
                floors = Floor.query.filter_by(id=room.floor_id).all()
                if floors:
                    for floor in floors:
                        location['floor_name'] = floor.name
                        build = Building.query.filter_by(
                            id=floor.building_id).all()
                        if build is not None:
                            location['build_name'] = build[0].name
                            locaList.append(location)
                        else:
                            return {'status': 'the building not exit'}
                else:
                    return {'status': 'the floor not exit'}

        else:
            return {'status': 'the room not exit'}

        return locaList


class time_data(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('build_name', type=unicode)
        parser.add_argument('floor_name', type=str)
        parser.add_argument('room_name', type=str)
        parser.add_argument("start_time", type=str)
        parser.add_argument("end_time", type=str)
        args = parser.parse_args(strict=True)
        buildInfor = Building.query.filter_by(
            name=args['build_name']).first_or_404()
        if buildInfor:
            floorInfor = Floor.query.filter_by(
                name=args['floor_name'],
                building_id=buildInfor.id).first_or_404()
            if floorInfor:
                roomInfor = Room.query.filter_by(
                    name=args['room_name'],
                    floor_id=floorInfor.id).first_or_404()
                if roomInfor:
                    deviceInfor = Device.query.filter_by(
                        room_id=roomInfor.id).first_or_404()
        if deviceInfor:
            results = SensorData.query.filter(
                SensorData.datetime >= args['start_time'],
                SensorData.datetime <= args['end_time'],
                SensorData.device_id == deviceInfor.id
            ).order_by('datetime desc').all()
            # values = to_json_list(results)
            sensor_list = []
            for result in results:
                value = {}
                value["sensor"] = Sensor.query.filter_by(
                    id=result.sensor_id).first().name
                value["time"] = str(result.datetime)
                value["value"] = str(result.value)
                sensor_list.append(value)
                print sensor_list
        return sensor_list, 200


class timeSerial(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("start_time", type=str)
        parser.add_argument('end_time', type=str)
        args = parser.parse_args(strict=True)
        sensorValues = SensorData.query.filter(
            SensorData.datetime >= args['start_time'],
            SensorData.datetime <= args['end_time']
        ).order_by('datetime desc').all()
        sensorList = []
        for value in sensorValues:
            sensor = {}
            sensor["room"] = value.device.room.name
            sensor["floor"] = value.device.room.floor.name
            sensor["building"] = value.device.room.floor.building.name
            sensor["longitude"] = value.device.room.floor.building.longitude
            sensor["latitude"] = value.device.room.floor.building.latitude
            sensor["name"] = value.sensor.name
            sensor["value"] = value.value
            sensor['datetime'] = str(value.datetime)
            sensorList.append(sensor)
        return sensorList, 200


class sensorLocation(Resource):

    def get(self):
        records = Device.query.all()
        locations = []
        for record in records:
            location = {}
            location["room_name"] = record.room.name
            location["floor_name"] = record.room.floor.name
            location["building_name"] = record.room.floor.building.name
            locations.append(location)
        return locations, 200


class deviceData(Resource):

    def get(self):
        try:
            uuid = request.args.get('uuid')
            start_time = request.args.get('start_time')
            end_time = request.args.get('end_time')
            count = request.args.get('count')
            if count is None:
                count = 4
            sensorValues = SensorData.query.filter(
                SensorData.datetime >= start_time,
                SensorData.datetime <= end_time,
                SensorData.device_id == uuid
            ).order_by('datetime desc').limit(count)
            sensorList = []
            for value in sensorValues:
                sensor = {}
                sensor["room"] = value.device.room.name
                sensor["floor"] = value.device.room.floor.name
                sensor["building"] = value.device.room.floor.building.name
                sensor["name"] = value.sensor.name
                sensor["value"] = value.value
                sensor['datetime'] = value.datetime
                sensor['ele_quantity'] = value.ele_quantity
                sensor['device_temp'] = value.device_temp
                sensor['voltage'] = value.voltage
                sensorList.append(sensor)
            return sensorList, 200
        except:
            return {"error": "the url is invalid!"}

