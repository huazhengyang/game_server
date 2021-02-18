#! -*- coding:utf-8 -*-
# Time : 2021/1/27 7:22 下午 
# Author : borland83@126.com
# File : pokergame.py 
# Comment: 
# Software: PyCharm
from abc import ABC
from common.entity.game.gamebase import RSGame


class PokerGame(RSGame, ABC):
    """
    扑克游戏虚基类
    """
    def __init__(self, *args, **kwargs):
        super(RSGame, self).__init__()

    def init_game(self):
        pass

    def game_id(self):
        pass
