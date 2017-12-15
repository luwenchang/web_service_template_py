# -*- coding: utf-8 -*-
__author__ = 'vincent'

import json
from flask import jsonify, g, current_app
from flask_restful import Resource, reqparse
from app.utils import token_help, redis_help


class GetToken(Resource):
    def post(self):
        if g.token_used:
            g.logger.error('Token 登录用户禁止此项操作')
            return jsonify(
                {
                    'message': 'Token 登录用户禁止此项操作'
                }
            )
        expiration = 3600
        token = token_help.generate_auth_token(current_app.config['ICL_SECRET_KEY'], user_id=g.current_user['id'], expire=expiration)
        # 根据Token值，设置缓存用户信息的Key
        key = 'auth:token:{}'.format(token)
        # 缓存 用户信息
        token_help.set_token_cache(key, expiration, user=json.dumps(g.current_user))
        g.logger.info('Token 获取成功')
        return jsonify(
            {
                'token' : token ,
                'expiration' : expiration
            }
        )


class DeleteToken(Resource):
    def post(self):
        if not g.token_used: return jsonify({"message" : "未制定待释放的Token，请以待释放Token请求"})

        key = 'auth:token:{}'.format(g.currnet_token)
        token_help.delete_token_cache(key)
        g.logger.info('Token 当前用户的Token已删除')
        return jsonify(
            {
                'message': '当前用户Token已释放'
            }
        )

