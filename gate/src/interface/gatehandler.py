#! -*- coding:utf-8 -*-
# Time : 2021/1/21 7:33 下午 
# Author : borland83@126.com
# File : gatehandler.py 
# Comment: 
# Software: PyCharm
from rainstorm.util.decorator import mark_cmd_action_handler, mark_cmd_action_method

from gate.src.entity.chmanger import ChannelManger
from gate.src.entity.gatesession import gate_session
from common.utils.serverstate import ServerInfo


@mark_cmd_action_handler
class GateHandler(object):
    def _check_param_channel_map(self, msg, key, params):
        channel_map = msg.get_param(key)
        if isinstance(channel_map, dict):
            return None, channel_map
        return 'ERROR of {} {}'.format(self.__class__.__name__, 'channel_map'), channel_map

    def _check_param_scene_id(self, msg, key, params):
        scene_id = msg.get_param(key)
        if isinstance(scene_id, str):
            return None, scene_id
        return 'ERROR of {} {}'.format(self.__class__.__name__, 'scene_id'), scene_id

    def _check_param_server_info(self, msg, key, params):
        server_info = msg.get_param(key)
        if isinstance(server_info, dict):
            return None, server_info
        return 'ERROR of {} {}'.format(self.__class__.__name__, 'scene_id'), server_info

    @mark_cmd_action_method(cmd='channel', action='update')
    async def channel_update(self, channel_map):
        ChannelManger.channel_update(channel_map)

    @mark_cmd_action_method(cmd='heart_beat', action='heart_beat')
    async def heart_beat(self, server_type, server_id):
        pass

    @mark_cmd_action_method(cmd='user', action='login')
    async def user_login(self, server_type, server_id):
        pass

    @mark_cmd_action_method(cmd='server', action='state')
    async def server_state(self, server_info):
        ServerInfo.update_server_info(server_info)

    @mark_cmd_action_method(cmd='scene', action='change')
    async def scene_change(self, user_id, scene_id):
        gate_session.scene_change(user_id, scene_id)
