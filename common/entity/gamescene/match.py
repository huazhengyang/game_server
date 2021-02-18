#! -*- coding:utf-8 -*-
# Time : 2021/1/28 9:09 下午 
# Author : borland83@126.com
# File : match.py 
# Comment: 赛事
# Software: PyCharm
from abc import ABC
from common.entity.gamescene.room import RSRoom


class RSMatch(RSRoom, ABC):
    def __init__(self):
        super().__init__()