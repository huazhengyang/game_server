#! -*- coding:utf-8 -*-
# Time : 2021/2/3 8:13 下午 
# Author : borland83@126.com
# File : gateserver.py 
# Comment: 
# Software: PyCharm
from rainstorm.entity.server.tcpserver import RSTcpServer
from rainstorm.util import log as rslog
from rainstorm.entity.connection.connmanger import connection_manger_ins
from rainstorm.entity.configure.config import Test1, test, Configure
from rainstorm.support.singleton import Singleton


class GateServer(RSTcpServer, metaclass=Singleton):
    def __init__(self):
        super(RSTcpServer, self).__init__()

    def init_server(self, *args, **kwargs):
        rslog.debug("gate server start")
        print('client_manger_ins: ', len(connection_manger_ins.connections))

        print('Test1: ', Test1.test_list)
        print('Test2: ', test.test_list)
        print('Configure: ', Configure.global_conf)


def get_server_instance():
    return GateServer()