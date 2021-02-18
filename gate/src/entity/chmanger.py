#! -*- coding:utf-8 -*-
# Time : 2021/1/18 10:31 上午 
# Author : borland83@126.com
# File : chmanger.py 
# Comment: 发布频道管理
# Software: PyCharm
from rainstorm.util import log as rslog


class ChannelManger(object):
    channel_map = {}

    def __init__(self):
        pass

    @classmethod
    def channel_update(cls, channel_map):
        """
        更新发布频道列表
        :param channel_map:
        :return:
        """
        for key, value in channel_map.items():
            if key not in cls.channel_map:
                cls.channel_map[key] = value
            else:
                channel_list = cls.channel_map.get(key)
                if value == channel_list:
                    return

                new_channel_set = set(value)
                old_channel_set = set(channel_list)
                sub_channels = old_channel_set.difference(new_channel_set)
                for item in list(sub_channels):
                    channel_list.remove(item)
                add_channels = new_channel_set.difference(old_channel_set)
                channel_list.extend(list(add_channels))
                rslog.info('add channels: '.format(list(add_channels)))
