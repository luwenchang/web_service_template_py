# -*- coding: utf-8 -*-
__author__ = 'vincent'

import sys
import simplejson as json

import uuid
from flask import g, request
from flask import jsonify
from sqlalchemy.sql import or_
from sqlalchemy.sql import and_
from flask_httpauth import HTTPBasicAuth

from ..models.tb_main import User
from app.utils.loggers import get_logger

from . import api_bp

from ..utils import token_help
from app.utils import exceptions



reload(sys)
sys.setdefaultencoding("utf-8")


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(login_tag_account, password):
    '''验证用户密码'''
    # Token
    token = request.headers.get("X-Auth-Token")
    if token:
        # 此时属于验证token
        kvs = token_help.get_token_cache('auth:token:{}'.format(token))

        # 不存在该Token
        if not kvs: return False
        user = json.loads(kvs.get('user'))

        g.token_used = True
        # 记录当前Token值
        g.current_token = token
        # g.current_user = User.query.filter_by(id=user_id).first()
        g.current_user = user
        return True

    else:
        # 获取 Body 数据
        body = request.get_json()
        # 验证 用户名密码
        if not body: return False

        # 实验室 ID
        lab_id = body.get('lab_id')
        # 用户名
        account = body.get('account')
        # 密码
        password = body.get('password')

        # 此时属于验证 用户名/密码
        if not lab_id or  not account or  not password:
            # 实验室ID 和 用户名  和 密码不能为空
            return False

        # 查找用户信息
        user = User.query.filter(
            and_(
                User.internalUserId == lab_id,
                or_(
                    User.username == account,
                    User.mobile == account,
                    User.email == account
                )
            )
        ).first()
        if not user:
            # 未找到指定用户
            g.current_user = None
            return False

        if not user.verify_password(password):
            # 密码错误
            g.current_user = None
            return False

        g.token_used = False
        g.current_token = None
        cur_user = user.to_dict()
        g.current_user = {
            'id' : cur_user['id'],
            'internalUserId' : cur_user['internalUserId'],
            'groupId' : cur_user['groupId'],
            'isLabUser' : cur_user['isLabUser'],
            'isIndependent' : cur_user['isIndependent'],
            'noBalanceQuota' : cur_user['noBalanceQuota'],
            'isDisabled' : cur_user['isDisabled'],
        }

    return True




@auth.error_handler
def auth_error():
    return jsonify({
        "code" : "LoginField",
        "message" : "登陆验证失败"
    })


# 通过如下方法，api 蓝本中所有路由都能进行自动认证。
# 而且作为附加认证，before_request 处理程序还会拒绝已通过认证，但没有确认账户的用户
@api_bp.before_request
@auth.login_required
def before_request():
    g.request_id = str(uuid.uuid4())
    g.logger = get_logger(g.request_id)
    if not g.current_user:
        g.logger.warning(str(exceptions.LoginFailed()))
        return jsonify(exceptions.LoginFailed().dict)

    elif g.current_user.get('isDisabled'):
        g.logger.warning(str(exceptions.AccountDisabled()))
        return jsonify(exceptions.AccountDisabled().dict)
    else:
        g.logger.info('权限验证成功')





