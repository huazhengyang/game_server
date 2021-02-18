#! -*- coding:utf-8 -*-
# Time : 2021/2/7 3:07 下午 
# Author : borland83@126.com
# File : scenemgr.py 
# Comment: 
# Software: PyCharm
from rainstorm.entity.message.msg import MsgPack
from rainstorm.entity.message.msgtransfer import MsgTransfer

from common.entity.session import SessionData
from common.entity.database.userdata import UserSession
from common.entity.database.daoconst import SessionKey
from common.utils.const import GameId

from scene.sceneserver import get_server_instance


class SceneMgr(object):
    @classmethod
    def get_scene_id(cls):
        # 获取当前的场景id
        scene_server = get_server_instance()
        if not scene_server:
            raise Exception('scene server is not exists!')

        server_type, server_id = scene_server.get_type_and_id()
        return server_type + server_id

    @classmethod
    async def scene_enter(cls, user_id, game_id):
        """
        进入场景，更新场景信息
        :param user_id:
        :return:
        """
        scene_id = cls.get_scene_id()

        # 更新redis场景信息
        await UserSession.set_session_multi(user_id, SessionKey.SESSION_SCENEID, scene_id,
                                            SessionKey.SESSION_GAMEID, game_id)

        # 更新本服场景信息
        await SessionData.update_session(user_id, scene_id)

        # 根据当前场景回复消息给客户端
        server_type = GameId.get_server_type(game_id)
        if not server_type:
            raise Exception('Incorrect game id, game_id: {}'.format(game_id))

        # todo 回复场景信息


    @classmethod
    def scene_leave(cls, user_id):
        """
        离开场景，更新场景信息
        :param user_id:
        :return:
        """
        SessionData.del_session(user_id)

