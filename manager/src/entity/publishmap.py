#! -*- coding:utf-8 -*-
# Time : 2021/1/13 9:34 下午 
# Author : borland83@126.com
# File : publishmap.py 
# Comment: 
# Software: PyCharm


class PublishMap(object):
    publish_map = None

    @classmethod
    def init(cls, channel_map):
        cls.publish_map = channel_map

    @classmethod
    def send_pub_channels(cls):
        pass
