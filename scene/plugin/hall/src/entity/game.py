#! -*- coding:utf-8 -*-
# Time : 2021/2/4 7:22 下午 
# Author : borland83@126.com
# File : game.py 
# Comment: 
# Software: PyCharm
from rainstorm.util import log as rslog
from common.entity.game.gamebase import RSGame


class Hall(RSGame):
    def __init__(self):
        rslog.debug('hall instance begin!')