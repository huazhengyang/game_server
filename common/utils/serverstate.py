#! -*- coding:utf-8 -*-
# Time : 2021/2/9 3:43 下午 
# Author : borland83@126.com
# File : serverstate.py 
# Comment: 
# Software: PyCharm
from rainstorm.entity.lock import RSLock


class ServerInfo(object):
    """
    存储服务状态信息
    {
        'hall': [
            ('hall001', 80),
            ('hall002', 70)
        ],
        'texas': [
            ('texas002', 30),
            ('texas001', 20)
        ],
        'baccarat': [
            ('baccarat001', 65),
            ('baccarat002', 60)
        ]
    }
    """
    server_info = {}
    locker = RSLock()

    @classmethod
    def update_server_info(cls, server_info):
        """
        更新最新的服务信息
        :param server_info:
        :return:
        """
        with cls.locker:
            for key, value in server_info.items():
                server_type = key[0:-3]
                if server_type not in cls.server_info:
                    temp = [(key, value)]
                    cls.server_info[server_type] = temp
                else:
                    cls.server_info[server_type].append((key, value))

            def take_second(elem):
                return elem[1]

            for key, value in cls.server_info.items():
                value.sort(key=take_second, reverse=True)

    @classmethod
    def get_best_server(cls, server_type):
        """
        获取最佳的服务器
        :param server_type:
        :return:
        """
        server_list = cls.server_info.get(server_type, None)
        if not server_list:
            return None, None

        return server_list
