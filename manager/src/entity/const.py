#! -*- coding:utf-8 -*-
# Time : 2021/1/13 3:14 下午 
# Author : borland83@126.com
# File : const.py 
# Comment: 
# Software: PyCharm

SERVER_HEART_BEAT_INTERVAL = 5  #服务器检测心跳间隔
SERVER_OUT_OF_LINE_TICK = 3 #超过几个tick没有更新心跳则视为服务下线
SERVER_ONLINE_TICK = 3 #超过几个tick的服务仍然是健康的则视为可用