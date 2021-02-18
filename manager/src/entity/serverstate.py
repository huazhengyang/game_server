#! -*- coding:utf-8 -*-
# Time : 2021/1/13 9:33 下午 
# Author : borland83@126.com
# File : serverstate.py 
# Comment: 
# Software: PyCharm
import time
from typing import NoReturn

from rainstorm.entity.timer import RSTimerLoop
from rainstorm.util import log as rslog
from rainstorm.entity.message.msgtransfer import MsgTransfer
from rainstorm.entity.message.msg import MsgPack

from manager.src.entity.const import SERVER_HEART_BEAT_INTERVAL, SERVER_OUT_OF_LINE_TICK
from manager.src.entity.publishmap import PublishMap


class ServerState(object):
    def __init__(self):
        self._server_type = None
        self._server_id = None
        self._server_score = None
        self._alive_time = None
        self._register_time = None
        self._is_using = False

    @property
    def server_type(self) -> NoReturn:
        return self._server_type

    @server_type.setter
    def server_type(self, value: str) -> NoReturn:
        self._server_type = value

    @property
    def server_id(self):
        return self._server_id

    @server_id.setter
    def server_id(self, value):
        self._server_id = value

    @property
    def server_score(self):
        return self._server_score

    @server_score.setter
    def server_score(self, value):
        self._server_score = value

    @property
    def alive_time(self):
        return self._alive_time

    @alive_time.setter
    def alive_time(self, value):
        self._alive_time = value

    @property
    def register_time(self):
        return self._register_time

    @register_time.setter
    def register_time(self, value: int):
        self._register_time = value

    @property
    def is_using(self):
        return self._is_using

    @is_using.setter
    def is_using(self, value: bool):
        self._is_using = value

    @staticmethod
    def cal_server_score() -> int:
        """
        根据服务器状态值结算服务评分
        :return:
        """
        # todo 根据服务器的状态计算评分
        return 100


class ServerStateManger(object):
    """
    维护服务器状态列表
    server_state = {
        'Gate001': {
            'server_type': Gate,            服务器类型
            'server_id': 1610626411,        服务编号
            'server_score': 100,            服务器评分
            'alive_time': 1610626411,       最后一次收到心跳的时间
            'register_time': 1610626414,    服务器注册时间
            'is_using': True,               是否已启用，即是否将其加入列表发送给网关或者sdk用来处理消息
        }
    }
    服务器列表
    server_map = {
        'Gate': [
            '001',
            '002',
            '003'
        ],
        'Hall': [
            '001',
            '002'
        ]
    }
    """
    server_state = {}
    server_map = {}

    @classmethod
    def _find_server_info(cls, server_flag: str) -> int:
        return cls.server_state.get(server_flag, None)

    @classmethod
    def check_server(cls, server_type, server_id):
        """
        检查并更新所有当前发送心跳的服务器状态
        :param server_type:
        :param server_id:
        :return:
        """
        # todo 考虑是否需要加锁
        server_flag = server_type + server_id
        server = cls._find_server_info(server_flag)
        if server is None:
            server_info = ServerState()
            server_info.server_type = server_type
            server_info.server_id = server_id
            server_info.server_score = ServerState.cal_server_score()
            server_info.alive_time = int(time.time())
            server_info.register_time = int(time.time())
            server_info.is_using = False
            cls.server_state[server_flag] = server_info
        else:
            if isinstance(server, ServerState):
                server.server_score = ServerState.cal_server_score()
                server.alive_time = int(time.time())
            else:
                raise TypeError('Error type, server_info!')

        if server.is_using:
            cls.send_logic_server_state(server_type, server_id)

    @classmethod
    def remove_server(cls, server_flag):
        server_info = cls._find_server_info(server_flag)
        if server_info:
            del cls.server_state[server_flag]

    @classmethod
    def get_alive_time(cls, server_flag):
        server_info = cls._find_server_info(server_flag)
        if server_info:
            return server_info.alive_time

        return None

    @classmethod
    def get_register_time(cls, server_flag):
        server_info = cls._find_server_info(server_flag)
        if server_info:
            return server_info.register_time

        return None

    @classmethod
    def get_server_score(cls, server_flag):
        server_info = cls._find_server_info(server_flag)
        if server_info:
            return server_info.server_score

        return None

    @classmethod
    def get_is_using(cls, server_flag):
        server_info = cls._find_server_info(server_flag)
        if server_info:
            return server_info.is_using

        return None

    @classmethod
    def get_server_type(cls, server_flag):
        server_info = cls._find_server_info(server_flag)
        if server_info:
            return server_info.server_type

        return None

    @classmethod
    def get_server_id(cls, server_flag):
        server_info = cls._find_server_info(server_flag)
        if server_info:
            return server_info.server_id

        return None

    @classmethod
    def add_server(cls, server_type, server_id):
        servers = cls.server_map.get(server_type, None)
        if not servers:
            servers = [server_id]
            cls.server_map[server_type] = servers
        else:
            if server_id in servers:
                rslog.warning('server already in server_map, server_type: {}, server_id: {}'.format(server_type,
                                                                                                    server_id))
                return
            servers.append(server_id)

    @classmethod
    def send_logic_server_state(cls, server_type, server_id):
        """
        向场景服务器发送场景服务器状态
        :return:
        """
        server_info = {}
        server_flag = server_type + server_id
        for key, value in cls.server_state.items():
            if server_flag != key and value.is_using:
                # 不保存同类型的服务信息
                server_info[key] = value.server_score

        msg = MsgPack()
        msg.set_cmd('server')
        msg.set_action('state')
        msg.set_param('server_info', server_info)

        MsgTransfer.router_to_server_in_loop(server_flag, msg)


class ServerCheck(object):
    """
    服务器状态检测
    """
    def __init__(self):
        self.loop_timer = None

    def start(self):
        self.loop_timer = RSTimerLoop(self.server_check, SERVER_HEART_BEAT_INTERVAL)
        self.loop_timer.start()

    def server_check(self):
        if not ServerStateManger.server_state:
            return

        rslog.debug('server_map: {}'.format(ServerStateManger.server_map))
        curr_time = int(time.time())
        # 注意在循环中删除字典元素要使用list循环，否则会引发迭代器失效
        for server_flag in list(ServerStateManger.server_state.keys()):
            alive_time = ServerStateManger.get_alive_time(server_flag)
            if alive_time is None:
                rslog.error('can not get server alive time, server_flag: {}'.format(server_flag))
                continue

            dead_interval = curr_time - alive_time
            rslog.debug('curr_time: {}, alive_time: {}, server_flag: {}'.format(int(time.time()),
                                                                                alive_time, server_flag))
            if dead_interval > SERVER_OUT_OF_LINE_TICK * 3:
                # 距离上次更新心跳3个tick以上，则视为服务不可用，移除服务器
                rslog.info('server is dead, server_flag: {}'.format(server_flag))
                ServerStateManger.remove_server(server_flag)
                continue

            register_time = ServerStateManger.get_register_time(server_flag)
            if register_time is None:
                rslog.error('can not get server register time, server_flag: {}'.format(server_flag))
                continue

            is_using = ServerStateManger.get_is_using(server_flag)
            if is_using is None:
                rslog.error('can not get server is_using, server_flag: {}'.format(server_flag))
                continue

            alive_interval = curr_time - register_time
            if alive_interval > SERVER_OUT_OF_LINE_TICK * 3 and not is_using:
                # 服务度过健康观察期，并且没有使用，则将其状态设置为可用
                ServerStateManger.server_state[server_flag].is_using = True
                server_type = ServerStateManger.get_server_type(server_flag)
                server_id = ServerStateManger.get_server_id(server_flag)
                ServerStateManger.add_server(server_type, server_id)

        # todo 向网关发送游戏服务器(hall, game)状态列表

        # todo 向sdk发送网关服务器状态列表

        # 向所有服务器发送对应的发布频道列表
        self.send_pub_channel_list()

        # todo 后续可以计算同一类型的服务器的平均分，如果平均分低，则代表服务器压力大，发消息给守护进程，增加服务，以均衡负载，这个可以最后做
        # todo 守护进程啥也不干，就看那个进程挂了，把它重启或者启动新的服务进程

    @staticmethod
    def send_pub_channel_list():
        """
        发送发布频道列表
        :return:
        """
        for key, values in ServerStateManger.server_map.items():
            print(key, values)
            server_pub_list = PublishMap.publish_map.get(key, None)
            print('server_pub_list: ', server_pub_list)
            if not server_pub_list:
                continue

            for item in values:
                channels_map = {}
                for server_channel in server_pub_list:
                    channels = ServerStateManger.server_map.get(server_channel)
                    if channels:
                        channels_map[server_channel] = channels

                if channels_map:
                    server_flag = key + item
                    print('server_flag', server_flag)
                    msg = MsgPack()
                    msg.set_cmd('channel')
                    msg.set_action('update')
                    msg.set_param('channel_map', channels_map)

                    MsgTransfer.router_to_server_in_loop(server_flag, msg.pack())

    def send_logic_server_state(self):
        """
        向网关服务器发送逻辑服务器状态(hall, game等)
        :return:
        """
        pass

    def send_gate_server_state(self):
        """
        向sdk发送网关状态
        :return:
        """
        pass

    def server_check_stop(self):
        self.loop_timer.stop()

