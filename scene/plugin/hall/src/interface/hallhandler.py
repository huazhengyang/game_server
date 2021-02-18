#! -*- coding:utf-8 -*-
# Time : 2021/1/21 7:33 下午 
# Author : borland83@126.com
# File : hallhandler.py 
# Comment: 
# Software: PyCharm

from rainstorm.util.decorator import mark_cmd_action_handler, mark_cmd_action_method
from rainstorm.util import log as rslog

from common.entity.database.userdata import UserSession

from scene.sceneserver import get_server_instance
from scene.src.entity.sceneconst import GeneralConst


@mark_cmd_action_handler
class HallHandler(object):
    def _check_param_user_id(self, msg, key, params):
        user_id = msg.get_param(key)
        if isinstance(user_id, int):
            return None, user_id
        return 'ERROR of {} {}'.format(self.__class__.__name__, 'user_id'), user_id

    def _check_param_dest(self, msg, key, params):
        dest = msg.get_param(key)
        if isinstance(dest, str):
            return None, dest
        return 'ERROR of {} {}'.format(self.__class__.__name__, 'dest'), dest

    @mark_cmd_action_method(cmd='user', action='login')
    async def user_login(self, user_id, dest):
        # 测试客户端消息序列化，sleep了1秒
        hall_server = get_server_instance()
        #await asyncio.sleep(1)
        print(hall_server.server_type, hall_server.server_id)
        rslog.debug('recv user login msg!, user_id: {}, dest: {}'.format(user_id, dest))

        # ret = await UserRDData.run_user_cmd(10001, 'user:10001', 'session')
        # print('hall ret:', ret)

        # ret = await UserSession.get_session(user_id, GeneralConst.SESSION_IP)
        # print('hall ret:', ret)

        # ret = await UserSession.set_session_multi(user_id, GeneralConst.SESSION_PORT, 8080, GeneralConst.SESSION_GATE, '001')
        # print('hall ret:', ret)

        ret = await UserSession.get_session_multi(user_id, GeneralConst.SESSION_PORT, GeneralConst.SESSION_GATE, GeneralConst.SESSION_IP)
        print('hall ret:', ret)