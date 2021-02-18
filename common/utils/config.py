#! -*- coding:utf-8 -*-
# Time : 2021/1/29 8:25 下午 
# Author : borland83@126.com
# File : config.py 
# Comment: 基础库配置管理
# Software: PyCharm
from rainstorm.entity.configure.config import Configure
from rainstorm.entity.exception import ConfNotFindException


class CommonConfig(object):
    game_id = {}
    room_conf = {}
    table_conf = {}

    @classmethod
    def init(cls):
        cls.init_game_id(Configure.common_conf)

    @classmethod
    def init_game_id(cls, conf):
        game_id_conf = conf.get('gameid', None)
        if not game_id_conf:
            raise ConfNotFindException('not find common conf game_id')

        base_conf = game_id_conf.get('0', None)
        if not base_conf:
            raise ConfNotFindException('not find common conf game_id:0')

        cls.game_id = base_conf

    @classmethod
    def get_game_id(cls, key):
        return cls.game_id.get(key, None)

