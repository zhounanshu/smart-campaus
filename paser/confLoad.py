#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-
import json
import os
import logging
from util import init_logging


class confLoader(object):

    def __init__(self):
        init_logging()
        self.path = os.path.split(
            os.path.realpath(__file__))[0] + '/config.json'
        with open(self.path) as f:
            configInfor = json.load(f)
        if configInfor is not None:
            self.host = configInfor['host']
            self.port = configInfor['port']
            self.user = configInfor['user']
            self.passwd = configInfor['passwd']
            self.db = configInfor['db']
        else:
            logging.debug("load config failed......")

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def get_user(self):
        return self.user

    def get_passwd(self):
        return self.passwd

    def get_db(self):
        return self.db
