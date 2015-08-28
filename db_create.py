#!usr/bin/env python
# -*- coding: utf-8 -*-
from app import create_app
from app import db
from instance.config import *

cnf = ProductionConfig
app = create_app(cnf)
with app.app_context():
    db.create_all(app=app)
