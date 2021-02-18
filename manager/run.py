#! -*- coding:utf-8 -*-
# Time : 2021/1/11 8:00 下午 
# Author : borland83@126.com
# File : run.py.py 
# Comment: 
# Software: PyCharm

from rainstorm.entity.server.runserver import start_server
from manager.src.server.managerserver import ManagerServer

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print('Usage: pypy run.py config_path server_type server_id')
    #     exit(1)
    #
    # config_path = sys.argv[1]
    # server_type = sys.argv[2]
    # server_id = sys.argv[3]
    #
    # start_server(
    #     server_class=RSTCPServer,
    #     server_init=GateServer.init_server,
    #     config_path=config_path,
    #     server_type=server_type,
    #     server_id=server_id)

    start_server(ManagerServer,
                 ManagerServer.init_server,
                 config_path="/Users/huazhengyang/Documents/iCollections/pythonCode/poker-server/config",
                 server_type='manager',
                 server_id='001',
                 port=11001)
