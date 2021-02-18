#! -*- coding:utf-8 -*-
# Time : 2021/2/3 8:10 下午 
# Author : borland83@126.com
# File : managerserver.py 
# Comment: 
# Software: PyCharm
import os

from rainstorm.entity.server.tcpserver import RSTcpServer
from rainstorm.entity.configure.config import Configure
from rainstorm.util import log as rslog
from manager.src.entity.serverstate import ServerCheck
from manager.src.entity.publishmap import PublishMap


class ManagerServer(RSTcpServer):
    def __init__(self):
        super(RSTcpServer, self).__init__()
        self.server_list = []
        self.pub_channels = {}
        self.server_check = None

    def init_server(self, *args, **kwargs):
        # 服务配置初始化
        try:
            # todo 这需要想下，配置文件如何更好的管理，暂时各个服务读取自己的配置文件,后面要改成全部存入redis
            config_dir_path = kwargs['config_path'] + '/' + 'Server'
            server_conf = self.get_server_config(config_dir_path)
            PublishMap.publish_map = server_conf.get('pub_channels', None)
            if PublishMap.publish_map is None:
                raise Exception('pub_channels conf is not exists!')

            # 初始化服务器健康检查
            self.server_check = ServerCheck()
            self.server_check.start()

            # todo 初始化发布频道列表
        except Exception as e:
            rslog.error('init server failed. server type: {}, server id: {}'.format(self.server_type, self.server_id))
            raise e

    def stop(self):
        super().stop()
        self.server_check.server_check_stop()

    def get_server_config(self, config_dir_path):
        server_conf = None
        for file in os.listdir(config_dir_path):
            file_name, _ = os.path.splitext(file)
            if file_name == self.server_type:
                abs_file_path = os.path.join(config_dir_path, file)
                server_conf = Configure.parse_config_file(abs_file_path)
                break
        return server_conf
