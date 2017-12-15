# -*- coding: utf-8 -*-
__author__ = 'vincent'


from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import toolkit

'''
# 用户模型必须实现 82页：表8-1 所需要的四个方法，如下：
# is_authenticated 如果用户已登录，则返回True，否则返回False
# is_active 如果允许用户登录，则返回True，否则返回False
# is_anonymous 对普通用户必须返回False
# get_id 必须返回用户的唯一标示符，使用unicode 编码字符串
可以使用 Flask-Login 提供的UserMixin类，就自动拥有以上四种方法了
'''
from flask_login import UserMixin
from flask_login import AnonymousUserMixin

# 下面这个包 itsdangerous 用于生成确认令牌
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask import request
from flask import url_for

from sqlalchemy.sql import and_
from sqlalchemy.sql import or_
from .. import Cfg

from .. import db



class TableBase:
    # 所有表公共字段
    seq = db.Column(db.Integer, primary_key=True)

    # createTimestamp = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    # updateTimestamp = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    createTimestamp = db.Column(db.TIMESTAMP(True), nullable=False, server_default=db.text("UTC_TIMESTAMP"))
    updateTimestamp = db.Column(db.TIMESTAMP(True), nullable=False, server_default=db.text("UTC_TIMESTAMP ON UPDATE UTC_TIMESTAMP"))

    # 允许展示的字段列表
    _to_dict_default_fields_ = []

    def to_dict(self, fields=[]):
        return toolkit.filter_table_field(self.__dict__, fields if fields else self._to_dict_default_fields_)

