#! -*- coding:utf-8 -*-
# Time : 2021/2/5 7:25 下午 
# Author : borland83@126.com
# File : scenehandler.py 
# Comment: 
# Software: PyCharm

from rainstorm.util.decorator import mark_cmd_action_handler, mark_cmd_action_method
from rainstorm.util import log as rslog

from common.utils.serverstate import ServerInfo

from scene.src.entity.scenemgr import SceneMgr


@mark_cmd_action_handler
class SceneHandler(object):
    def _check_param_user_id(self, msg, key, params):
        user_id = msg.get_param(key)
        if isinstance(user_id, int):
            return None, user_id
        return 'ERROR of {} {}'.format(self.__class__.__name__, 'user_id'), user_id

    def _check_param_game_id(self, msg, key, params):
        game_id = msg.get_param(key)
        if isinstance(game_id, int):
            return None, game_id
        return 'ERROR of {} {}'.format(self.__class__.__name__, 'game_id'), game_id

    @mark_cmd_action_method(cmd='scene', action='enter')
    async def scene_enter(self, user_id, game_id):
        await SceneMgr.scene_enter(user_id, game_id)

    @mark_cmd_action_method(cmd='scene', action='leave')
    async def scene_leave(self, user_id):
        SceneMgr.scene_leave(user_id)

    @mark_cmd_action_method(cmd='server', action='state')
    async def server_state(self, server_info):
        ServerInfo.update_server_info(server_info)
