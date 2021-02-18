#! -*- coding:utf-8 -*-
# Time : 2020/12/24 11:22 上午 
# Author : borland83@126.com
# File : sdk_server.py 
# Comment: 
# Software: PyCharm

from gate import RSHttpServer
from gate import DaoBase
from gate import config
from gate import Singleton


class SdkServer(RSHttpServer, metaclass=Singleton):
    @staticmethod
    def init_server(*args, **kwargs):
        config.init_global_config(kwargs['config_path'])
        DaoBase.init_mongo()
