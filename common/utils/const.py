#! -*- coding:utf-8 -*-
# Time : 2021/2/9 5:07 下午 
# Author : borland83@126.com
# File : const.py 
# Comment: 
# Software: PyCharm

HALL_GAME_ID = 9999
TEXAS_GAME_ID = 101
BACCARAT_GAME_ID = 102


class GameId(object):
    game_map = {
        HALL_GAME_ID: 'hall',
        TEXAS_GAME_ID: 'texas',
        BACCARAT_GAME_ID: 'baccarat'
    }

    @classmethod
    def get_server_type(cls, game_id):
        return cls.game_map.get(game_id, None)