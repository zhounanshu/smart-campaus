#!/usr/bin/env python
# -*- coding: utf-8 -*-
# al
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    # password_hash = db.Column(db.String(128))
    passwd = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, username, password, email):
        self.name = username
        # self.password = password
        self.passwd = password
        self.email = email

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    # @password.setter
    # def password(self, passw):
    #     self.password_hash = generate_password_hash(passw)

    # def verify_password(self, passw):
    #     return check_password_hash(self.password_hash, passw)


class Building(db.Model):
    __tablename__ = 'building'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    description = db.Column(db.String(255))
    relationship = db.relationship('Floor', backref='building', lazy='dynamic')

    def __init__(self, name, latitude, longitude, description):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.description = description


class Floor(db.Model):
    __tablename__ = 'floor'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    building_id = db.Column(
        db.Integer, db.ForeignKey('building.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    relationship = db.relationship('Room', backref='floor', lazy='dynamic')

    def __init__(self, building_id, name, description):
        self.building_id = building_id
        self.name = name
        self.description = description


class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    relationship = db.relationship('Device', backref='room', lazy='dynamic')

    def __init__(self, floor_id, name, description):
        self.floor_id = floor_id
        self.name = name
        self.description = description


class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    name = db.Column(db.String(255))
    uuid = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    relationship = db.relationship(
        'SensorData', backref='device', lazy='dynamic')

    def __init__(self, room_id, name, uuid, description):
        self.room_id = room_id
        self.uuid = uuid
        self.name = name
        self.description = description


class Sensor(db.Model):
    __tablename__ = 'sensor'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    relationship = db.relationship(
        'SensorData', backref='sensor', lazy='dynamic')

    def __init__(self, name, type, description):
        self.name = name
        self.type = type
        self.description = description


class SensorData(db.Model):
    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sensor_id = db.Column(
        db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    device_id = db.Column(
        db.String(255), db.ForeignKey('device.uuid'), nullable=False)
    value = db.Column(db.String(255))
    datetime = db.Column(db.String(255))
    ele_quantity = db.Column(db.String(255))
    voltage = db.Column(db.String(255))
    device_temp = db.Column(db.String(255))

    def __init__(self, sensor_id, device_id,
                 value, datetime, ele_quantity,
                 voltage, device_temp):
        self.sensor_id = sensor_id
        self.device_id = device_id
        self.value = value
        self.datetime = datetime
        self.ele_quantity = ele_quantity
        self.voltage = voltage
        self.device_temp = device_temp

# Create the database tables.
# db.create_all()
