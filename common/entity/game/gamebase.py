#! -*- coding:utf-8 -*-
# Time : 2021/1/28 9:31 下午 
# Author : borland83@126.com
# File : gamebase.py 
# Comment: 
# Software: PyCharm
import abc
from rainstorm.entity.event.event_bus import RSEventBus


class RSGame(metaclass=abc.ABCMeta):
    """
    游戏虚基类
    """

    def __init__(self, *args, **kwargs):
        self._event_bus = RSEventBus()

    @abc.abstractmethod
    def init_game(self):
        pass

    @abc.abstractmethod
    def game_id(self):
        pass

    def get_event_bus(self):
        return self._event_bus
