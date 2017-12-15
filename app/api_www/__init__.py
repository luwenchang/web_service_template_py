# -*- coding: utf-8 -*-
__author__ = 'vincent'


from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api_www', __name__)

api = Api(api_bp)

from . import authentication

from .apis.token import GetToken

from .apis.user import GetUser
from .apis.user import SetUser




"""
@api {post} /GetToken 获取Token
@apiVersion 0.1.0
@apiName GetToken
@apiGroup auth

@apiHeader {String} account 帐号或token,格式 <实验室ID>/[<帐号>,<token>]:<password>

@apiParam {Number} id Users unique ID.

@apiSuccess {String} firstname Firstname of the User.
@apiSuccess {String} lastname  Lastname of the User.

@apiExample {Httpie} Httpie
    http  --json POST http://127.0.0.1:5000/wwwapi/v1/GetToken  lab_id=<lab_id> account=<account>  password=<password_md5>

@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
      "expiration": 3600,
      "token": "xxxxxxxxxxxxxxx"
    }

@apiError UserNotFound The <code>id</code> of the User was not found.

@apiErrorExample Error-Response:
    HTTP/1.1 500 Not Found
    {
        "message": "Internal Server Error"
    }
 """
api.add_resource(GetToken, '/GetToken')


"""
@api {post} /GetUser 获取用户信息
@apiVersion 0.1.0
@apiName GetUser
@apiGroup User

@apiParam {String} id Users unique ID.

@apiExample {Httpie} Httpie
    http  --json POST http://127.0.0.1:5000/wwwapi/v1/GetToken  X-Auth-Token:<token>
    
@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "avatarFileURL": null,
        "cache_labUserBalance": 1,
        "company": "xxxxxxx",
        "createTimestamp": "Mon, 27 Nov 2017 03:38:43 GMT",
        "email": "xxxx@qq.com",
        "groupId": "xxxxxxxxxxx",
        "id": "xxxxxxxxxxx",
        "internalUserId": "xxxxxxxxxxx",
        "intro": "",
        "isDisabled": 0,
        "isIndependent": 0,
        "isLabUser": 1,
        "labUserBalanceQuota": 20,
        "labUserSignInToken": "xxxxxx",
        "lastSeenTime": "Mon, 27 Nov 2017 03:46:54 GMT",
        "lastSignInTime": "Mon, 27 Nov 2017 03:42:17 GMT",
        "locale": "zh-CN",
        "mobile": "18621xxxxxxx",
        "name": "xxxxxxx",
        "noBalanceQuota": 0,
        "note": null,
        "position": "",
        "username": null
    }

@apiError UserNotFound The <code>id</code> of the User was not found.

@apiErrorExample Error-Response:
    HTTP/1.1 500 Not Found
    {
        "message": "Internal Server Error"
    }
 """
api.add_resource(GetUser, '/GetUser')



"""
@api {post} /SetUser 更新用户信息
@apiVersion 0.1.0
@apiName SetUser
@apiGroup User

@apiParam {String} id Users unique ID.


@apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "avatarFileURL": null,
        "cache_labUserBalance": 1,
        "company": "xxxxxxx",
        "createTimestamp": "Mon, 27 Nov 2017 03:38:43 GMT",
        "email": "xxx@qq.com",
        "groupId": "xxxxxxxxxxx",
        "id": "xxxxxxxxxxx",
        "internalUserId": "xxxxxxxxxxx",
        "intro": "",
        "isDisabled": 0,
        "isIndependent": 0,
        "isLabUser": 1,
        "labUserBalanceQuota": 20,
        "labUserSignInToken": "xxxxx",
        "lastSeenTime": "Mon, 27 Nov 2017 03:46:54 GMT",
        "lastSignInTime": "Mon, 27 Nov 2017 03:42:17 GMT",
        "locale": "zh-CN",
        "mobile": "18621xxxxxxx",
        "name": "xxxxxxx",
        "noBalanceQuota": 0,
        "note": null,
        "position": "",
        "username": null
    }

@apiError UserNotFound The <code>id</code> of the User was not found.

@apiErrorExample Error-Response:
    HTTP/1.1 500 Not Found
    {
        "message": "Internal Server Error"
    }
 """
api.add_resource(SetUser, '/SetUser')




