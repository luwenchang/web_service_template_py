# -*- coding: utf-8 -*-
__author__ = 'vincent'

import logging
from app import Cfg
#
# def getLogger(name):
#     logger = logging.getLogger(name)
#     watched_file_handler = logging.handlers.WatchedFileHandler(Cfg['logging']['file'])
#     watched_file_handler.setLevel(Cfg['logging']['level'])
#     watched_file_handler.setFormatter(logging.Formatter('%(name)s %(asctime)s %(levelname)8s %(message)s'))
#     logger.addHandler(watched_file_handler)
#     logger.setLevel(Cfg['logging']['level'])
#     return logger
#







import sys
import time
import logging

# 颜色设置
COLOR_RED    = '\033[1;31m'
COLOR_GREEN  = '\033[1;32m'
COLOR_YELLOW = '\033[1;33m'
COLOR_BLUE   = '\033[1;34m'
COLOR_PURPLE = '\033[1;35m'
COLOR_CYAN   = '\033[1;36m'
COLOR_GRAY   = '\033[1;37m'
COLOR_WHITE  = '\033[1;38m'
COLOR_RESET  = '\033[1;0m'

# 设置日志级别颜色
LOG_COLORS = {
    'DEBUG'  : COLOR_BLUE,
    'INFO'   : COLOR_GREEN,
    'WARNING': COLOR_YELLOW,
    'ERROR'  : COLOR_RED
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color_cap = LOG_COLORS[record.levelname]
        log_time = time.localtime(record.created)
        log_time = time.strftime('%Y/%m/%d %H:%M:%S', log_time)

        log_line = '{}{} [{}][{}]\033[0m {}'.format(
            color_cap,
            log_time,
            record.levelname,
            record.name,
            record.msg)

        return log_line

# 设置日志流数据流向
log_hander = logging.StreamHandler(stream=sys.stdout)
# 设置日志级别
log_hander.setLevel(logging.DEBUG)
# 设置日志格式信息
log_hander.setFormatter(ColoredFormatter())

def get_logger(logger_name=None):
    '''
    获取日志对象
    '''
    if not logger_name:
        logger_name = 'SYSTEM'

    logger = logging.getLogger(logger_name)

    if log_hander not in logger.handlers:
        logger.addHandler(log_hander)
        logger.setLevel(logging.DEBUG)

    return logger
