#! -*- coding:utf-8 -*-
# Time : 2021/2/3 8:11 下午 
# Author : borland83@126.com
# File : serverhandler.py 
# Comment: 
# Software: PyCharm
from rainstorm.util.decorator import mark_cmd_action_handler, mark_cmd_action_method
from manager.src.entity.serverstate import ServerStateManger


@mark_cmd_action_handler
class ManagerHandler(object):
    def _check_param_server_type(self, msg, key, params):
        server_type = msg.get_param(key)
        if isinstance(server_type, str):
            return None, server_type
        return 'ERROR of {} {}'.format(self.__class__.__name__, 'server_type')

    def _check_param_server_id(self, msg, key, params):
        server_id = msg.get_param(key)
        if isinstance(server_id, str):
            return None, server_id
        return 'ERROR of {} {}'.format(self.__class__.__name__, 'server_id')

    @mark_cmd_action_method(cmd='server', action='register')
    async def server_register(self, a, b):
        print("this is test_handler_one")

    @mark_cmd_action_method(cmd='heart_beat', action='heart_beat')
    async def heart_beat(self, server_type, server_id):
        ServerStateManger.check_server(server_type, server_id)