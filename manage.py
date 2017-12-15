#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vincent'

import os
import sys
from app import create_app, db
from app.models.tb_main import User, InternalUser


from flask_script import Manager, Shell
import logging

reload(sys)
sys.setdefaultencoding("utf-8")



app = create_app()
# 加载一些命令行工具包
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, InternalUser=InternalUser)
# 命令行工具- 新增一个命令行参数 shell ，自动加载 对象
manager.add_command('shell', Shell(make_context=make_shell_context))




if __name__ == '__main__':
    manager.run()