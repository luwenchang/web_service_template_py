# -*- coding: utf-8 -*-
__author__ = 'vincent'


import sys
import hashlib

def str_encrypt(str):
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(str)
    encrypts = sha.hexdigest()
    return encrypts

def get_salted_password_hash(salt, password, secret):
    """
    根据密码及相关信息获取加密后的摘要
    :param salt:
    :param password:
    :param secret:
    :return:
    """
    str_to_hash = '~{0}~{1}~{2}~'.format(salt, password, secret)
    hash = str_encrypt(str_to_hash)
    return hash

def get_password_md5(password):
    """通过MD5加密密码"""
    m2=hashlib.md5()
    m2.update(password)
    return m2.hexdigest()
