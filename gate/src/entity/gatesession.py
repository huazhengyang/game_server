#! -*- coding:utf-8 -*-
# Time : 2021/2/7 5:07 下午 
# Author : borland83@126.com
# File : gatesession.py 
# Comment: 
# Software: PyCharm
from rainstorm.entity.event import event_bus
from rainstorm.entity.event.event import EventClientConnect, EventClientSceneEnter
from rainstorm.entity.connection.connmanger import connection_manger_ins
from rainstorm.entity.message.msg import MsgPack
from rainstorm.entity.message.msgtransfer import MsgTransfer

from common.entity.database.userdata import UserSession
from common.entity.database.daoconst import SessionKey
from common.utils.const import GameId
from common.utils.serverstate import ServerInfo

from gate.src.server.gateserver import GateServer, get_server_instance


class GateSession(object):
    def __init__(self):
        event_bus.globalEventBus.subscribe(EventClientConnect, self.client_connect)
        event_bus.globalEventBus.subscribe(EventClientSceneEnter, self.client_scene_enter)

    async def client_connect(self, event):
        """
        gate逻辑层处理用户连接事件
        :param event:
        :return:
        """
        user_id = event.user_id
        ip = event.ip
        port = event.port
        await self.set_session(user_id, ip, port)

    @staticmethod
    async def set_session(user_id, ip, port):
        """
        设置session信息
        :return:
        """
        server_ins = get_server_instance()
        if not isinstance(server_ins, GateServer):
            raise Exception('server instance Error!, server_ins: {}'.format(type(server_ins)))

        gate = server_ins.get_server_flag()
        await UserSession.set_session_multi(user_id, SessionKey.SESSION_IP, ip, SessionKey.SESSION_PORT, port,
                                            SessionKey.SESSION_GATE, gate)

    @staticmethod
    async def client_scene_enter(event):
        """
        网关处理下客户端进入场景的事件
        :param event:
        :return:
        """
        game_id = event.game_id
        server_type = GameId.get_server_type(game_id)
        if not server_type:
            raise Exception('Incorrect game id, game_id: {}'.format(game_id))

        server, score = ServerInfo.get_best_server(server_type)
        if not server or not score:
            # 出错了
            mo = MsgPack()
            mo.set_cmd("scene")
            mo.set_result('action', 'enter')
            mo.set_result("game_id", game_id)
            mo.set_result("code", -1)
            await MsgTransfer.send_msg_to_user(mo)
            return

        # 将消息路由给正确的场景
        mo = MsgPack()
        mo.set_cmd("scene")
        mo.set_action('enter')
        mo.set_param("game_id", game_id)
        mo.set_param("user_id", event.user_id)
        await MsgTransfer.router_to_server(server, mo)

    @staticmethod
    def scene_change(user_id, scene_id):
        connection_manger_ins.update_scene_id(user_id, scene_id)


gate_session = GateSession()
