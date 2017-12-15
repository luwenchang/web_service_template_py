# -*- coding: utf-8 -*-
__author__ = 'vincent'

from .common import *
from datetime import datetime



class InternalUser(UserMixin, db.Model, TableBase):
    __tablename__ = 'users'

    seq = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(65), nullable=False, unique=True, server_default=db.text("''"))
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    mobile = db.Column(db.String(32), unique=True)
    passwordHash = db.Column(db.String(64))
    name = db.Column(db.String(512))
    company = db.Column(db.String(512))
    locale = db.Column(db.String(8), nullable=False, server_default=db.text("'zh-CN'"))
    intro = db.Column(db.Text)
    signInTime = db.Column(db.DateTime)
    seenTime = db.Column(db.DateTime)
    privilegeList = db.Column(db.Text, nullable=False)
    isDisabled = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))



    def verify_password(self, password):
        check_passwordHash = toolkit.get_salted_password_hash(
            self.id,
            password,
            Cfg.get('webServer', {}).get('secret'),
            Cfg.get('webServer', {}).get('str_format')
        )
        return self.passwordHash == check_passwordHash




class User(UserMixin, db.Model, TableBase):
    __tablename__ = 'tb_main_users'
    __table_args__ = (
        db.Index('email_internalUser', 'email', 'internalUserId', unique=True),
        db.Index('internalUser_token', 'internalUserId', 'labUserSignInToken'),
        db.Index('mobile_internalUser', 'mobile', 'internalUserId', unique=True)
    )

    seq = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(65), nullable=False, unique=True, server_default=db.text("''"))
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128))
    mobile = db.Column(db.String(32))
    passwordHash = db.Column(db.String(64))
    note = db.Column(db.Text)
    name = db.Column(db.String(512))
    company = db.Column(db.String(512))
    locale = db.Column(db.String(8), nullable=False, server_default=db.text("'zh-CN'"))
    position = db.Column(db.String(512))
    intro = db.Column(db.Text)
    groupId = db.Column(db.String(65))
    signInTime = db.Column(db.DateTime)
    seenTime = db.Column(db.DateTime)

    isDisabled = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))

    # 允许 to_dict 展示的字段列表
    _to_dict_default_fields_=['seq', 'id', 'internalUserId', 'labUserSignInToken', 'avatarFileURL', 'username', 'email',
                      'mobile', 'note', 'name', 'company', 'locale', 'position', 'intro', 'groupId',
                      'lastSignInTime', 'lastSeenTime', 'isLabUser', 'isIndependent', 'noBalanceQuota',
                      'labUserBalanceQuota', 'isDisabled', 'cache_labUserBalance',
                      'createTimestamp', 'updateTimestamp']

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.passwordHash = toolkit.get_salted_password_hash(
            self.id,
            password,
            Cfg.get('webServer', {}).get('secret'),
            Cfg.get('webServer', {}).get('str_format')
        )

    def verify_password(self, password):
        '''验证用户密码，注意这个password一定是经过md5加密的'''
        password_hash = toolkit.get_salted_password_hash(
            self.id,
            password,
            Cfg.get('webServer', {}).get('secret'),
            Cfg.get('webServer', {}).get('str_format')
        )
        if password_hash == self.passwordHash:
            return True
        else:
            return False

    def generate_confirmation_token(self, expiration=3600):
        '''生成一个用户令牌，有效期默认为1小时'''
        s = Serializer(current_app.config['ICL_TOKEN_SECRET_KEY'], expiration)
        return s.dumps({'confirm' : self.id, 'is_internal_user': False})

    def confirm(self, token):
        '''认证用户token'''
        s = Serializer(current_app.config['ICL_TOKEN_SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True

    def reset_password(self, new_password):
        '''重置密码'''
        self.password = new_password
        db.session.add(self)
        return True

    def change_email(self, new_email):
        '''重置邮件'''
        if new_email is None:
            return False

        if self.query.filter(and_(
            User.internalUserId == self.internalUserId,
            User.email == new_email)).first() is not None:
            # 新邮件在 当前实验室的用户列表中已存在
            return False
        # 更新邮件
        self.email = new_email
        db.session.add(self)
        return True

    def is_administrator(self):
        '''判断是否为管理员-外部站用户默认为False'''
        return False

    def ping(self):
        '''更新用户的最后一次访问时间'''
        self.lastSeenTime = datetime.utcnow()
        db.session.add(self)





