# -*- coding: utf-8 -*-
__author__ = 'vincent'

import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from configs.config import Cfg
from configs.config import Config

db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # 配置日志

    Config.init_app(app)

    # app 初始化 db
    db.init_app(app)


    # 注册蓝本 main
    from .api_www import api_bp as api_www_v1
    app.register_blueprint(api_www_v1, url_prefix='/wwwapi/v1')

    # 附加路由和自定义页面
    return app


