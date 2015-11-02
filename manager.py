#!/usr/bin/env python
# -*- coding: utf-8  -*-
from app import create_app
from flask.ext.script import Manager, Shell
from instance.config import *
from flask.ext.cors import CORS
# from app.models import db

cnf = ProductionConfig
app = create_app(cnf)
CORS(app)
# db.drop_all(app=app)
# db.create_all(app=app)
manager = Manager(app)


def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def deploy():
    """Run deployment tasks."""
    pass


if __name__ == '__main__':
    manager.run()
