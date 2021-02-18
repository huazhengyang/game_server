#! -*- coding:utf-8 -*-
# Time : 2021/1/23 4:19 下午 
# Author : borland83@126.com
# File : texashandler.py 
# Comment: 
# Software: PyCharm
from rainstorm.util.decorator import mark_cmd_action_handler, mark_cmd_action_method


@mark_cmd_action_handler
class TexasHandler(object):
    def _check_param_channel_map(self, msg, key, params):
        channel_map = msg.get_param(key)
        if isinstance(channel_map, dict):
            return None, channel_map
        return 'ERROR of {} {}'.format(self.__class__.__name__, 'channel_map'), channel_map

    @mark_cmd_action_method(cmd='texas', action='login')
    def user_login(self, user_id):
        pass