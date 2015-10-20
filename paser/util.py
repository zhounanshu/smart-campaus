#!/usr/bin/env pyhton
# -*- coding: utf-8 -*-
import logging

FORMAT = '%(asctime)s %(name)-6s %(levelname)-6s %(message)s'


def init_logging():
    logging.basicConfig(
        level=logging.DEBUG, format=FORMAT, datefmt="%y-%m-%d %H:%M:%S")
    pass
