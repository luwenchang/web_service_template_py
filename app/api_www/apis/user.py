# -*- coding: utf-8 -*-
__author__ = 'vincent'


from flask import jsonify, g, current_app
from flask_restful import Resource, reqparse, marshal_with, marshal_with_field


from app.utils import token_help, redis_help, toolkit

from app.models.tb_main import User

from app import db



class GetUser(Resource):
    def post(self):
        fields = ['id', 'internalUserId', 'labUserSignInToken', 'avatarFileURL', 'username', 'email', 'mobile',
                  'note', 'name', 'company', 'locale', 'position', 'intro', 'groupId',
                  'lastSignInTime', 'lastSeenTime', 'isLabUser', 'isIndependent', 'noBalanceQuota',
                  'labUserBalanceQuota', 'isDisabled', 'cache_labUserBalance',
                  'createTimestamp']

        user = User.query.filter_by(id=g.current_user['id']).first()
        g.logger.info('已获取用户信息')
        return jsonify(user.to_dict(fields))



parser = reqparse.RequestParser()
parser.add_argument('email', type=str, help='用户邮箱')
parser.add_argument('mobile', type=str, help='用户手机号')
parser.add_argument('avatarFileURL', type=str, help='用户头像')
parser.add_argument('note', type=str, help='备注')
parser.add_argument('company', type=str, help='公司名称')
parser.add_argument('intro', type=str, help='个人介绍')


class SetUser(Resource):
    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(id=g.current_user['id']).first()

        if args.get('email'):
            user.email = args.get('email')

        if args.get('mobile'):
            user.mobile = args.get('mobile')

        if args.get('avatarFileURL'):
            user.avatarFileURL = args.get('avatarFileURL')

        if args.get('note'):
            user.note = args.get('note')

        if args.get('company'):
            user.company = args.get('company')

        if args.get('intro'):
            user.intro = args.get('intro')

        db.session.add(user)
        db.session.commit()


        fields = ['id', 'internalUserId', 'labUserSignInToken', 'avatarFileURL', 'username', 'email', 'mobile',
                  'note', 'name', 'company', 'locale', 'position', 'intro', 'groupId',
                  'lastSignInTime', 'lastSeenTime', 'isLabUser', 'isIndependent', 'noBalanceQuota',
                  'labUserBalanceQuota', 'isDisabled', 'cache_labUserBalance',
                  'createTimestamp']

        return jsonify(user.to_dict(fields))