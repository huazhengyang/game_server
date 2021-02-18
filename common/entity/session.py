#! -*- coding:utf-8 -*-
# Time : 2021/2/4 3:03 下午 
# Author : borland83@126.com
# File : session.py 
# Comment: 管理场景服务的用户session信息
# Software: PyCharm
from common.entity.database.userdata import UserSession


class Session(object):
    def __init__(self, *args, **kwargs):
        self._ip = args[0]
        self._port = args[1]
        self._last_game = args[2]
        self._gate = args[3]
        self._online_state = args[4]
        self._device_id = args[5]
        self._scene_id = None

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def last_game(self):
        return self._last_game

    @property
    def gate(self):
        return self._gate

    @property
    def online_state(self):
        return self._online_state

    @property
    def device_id(self):
        return self._device_id

    @property
    def scene_id(self):
        return self._scene_id


class SessionData(object):
    session_data = {}

    def set_session(self):
        pass

    @classmethod
    def get_session(cls, user_id):
        return cls.session_data.get(user_id, None)

    @classmethod
    def get_gate(cls, user_id):
        session = cls.session_data.get(user_id, None)
        if not session:
            return session

        return session.gate

    @classmethod
    async def update_session(cls, user_id, scene_id):
        """
        更新session列表，
        如果表中不存在用户的session信息，则从redis中获取
        如果存在则更新scene_id，如果是场景服务这种情况是异常情况，说明上次用户离开这个场景是没有清除session信息
        如果是在网关服务，这种情况是正常的
        :param user_id:
        :param scene_id:
        :return:
        """
        user_session = cls.get_session(user_id)
        if not user_session:
            # 去redis中获取session信息
            session_info = await UserSession.get_session_without_scene(user_id)
            user_session = Session(list(session_info))
            cls.session_data[user_id] = user_session
        else:
            user_session.scene_id = scene_id

    @classmethod
    def del_session(cls, user_id):
        """
        删除用户的session信息
        :param user_id:
        :return:
        """
        user_session = cls.get_session(user_id)
        if user_session:
            del cls.session_data[user_id]