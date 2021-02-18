#! -*- coding:utf-8 -*-
# Time : 2020/12/29 8:30 下午 
# Author : borland83@126.com
# File : daoconst.py 
# Comment: 定义redis的key和一些常量，由于禁止redis的keys命令，所以新增的key要定义在这，便于查找
# Software: PyCharm


class RedisKey(object):
    SESSION_DATA = 'session:%s'
    GAME_DATA = 'gamedata:%s'
    USER_DATA = 'user:%s'


class SessionKey(object):
    SESSION_IP = 'ip'
    SESSION_PORT = 'port'
    SESSION_GATE = 'gate'
    SESSION_LAST_GAME = 'lg'
    SESSION_ONLINE_STATE = 'os'
    SESSION_DEVICEID = 'devId'
    SESSION_GAMEID = 'gameId'
    SESSION_SCENEID = 'sceneId'