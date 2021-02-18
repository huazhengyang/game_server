#! -*- coding:utf-8 -*-
# Time : 2021/1/28 8:00 下午 
# Author : borland83@126.com
# File : texas.py 
# Comment: 
# Software: PyCharm
from common.entity.game.pokergame import PokerGame

from common.utils.config import CommonConfig


class RSTexas(PokerGame):
    """
    德州扑克游戏类
    """
    def __init__(self, *args, **kwargs):
        super(RSTexas, self).__init__()
        self.game_id = CommonConfig.get_game_id('TEXAS_GAME_ID')

    def init_game(self):
        # todo 加载房间比赛系统
        self._load_rooms()

        self._load_tables()

        # todo 所有插件初始化，包括任务系统，道具系统的，函数名称必须一样
        pass

    @property
    def game_id(self):
        return self.game_id

    @game_id.setter
    def game_id(self, value):
        self._game_id = value

    def _load_rooms(self):
        pass

    def _load_tables(self):
        pass
