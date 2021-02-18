#! -*- coding:utf-8 -*-
# Time : 2021/2/3 7:14 下午 
# Author : borland83@126.com
# File : sceneserver.py 
# Comment: 
# Software: PyCharm
from rainstorm.entity.server.tcpserver import RSTcpServer
from rainstorm.support.singleton import Singleton
from rainstorm.util import log as rslog
from rainstorm.entity.configure.config import Configure
from rainstorm.entity.configure.globaldata import GlobalData
from rainstorm.entity.event.event_bus import RSEventBus

from common.entity.events import UserSecneChangeEvent
from common.utils.config import CommonConfig


class SceneServer(RSTcpServer, metaclass=Singleton):
    def __init__(self):
        super(RSTcpServer, self).__init__()
        self.event_bus = RSEventBus()
        self.event_bus.subscribe(UserSecneChangeEvent, self.user_scene_change)

    def init_server(self, *args, **kwargs):
        rslog.debug("scene server start")
        print("Configture: ", Configure.global_conf)

        # 初始化基础库配置
        CommonConfig.init()

        # 装载游戏插件
        self.load_game_plugin(GlobalData)

    @staticmethod
    def load_game_plugin(gdata):
        # 根据server_type查找对应目录下的插件文件
        print(gdata.get_game_packages())

    def user_scene_change(self, event):
        pass


def get_server_instance():
    return SceneServer()



