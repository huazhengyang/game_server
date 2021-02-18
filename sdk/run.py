#! -*- coding:utf-8 -*-
# Time : 2020/12/19 2:25 下午 
# Author : borland83@126.com
# File : run.py 
# Comment: 
# Software: PyCharm

from gate import start_server
from gate import Handler
from sdk.src.server.sdk_server import SdkServer

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
    #     server_class=RSHttpServer,
    #     server_init=init_server,
    #     config_path=config_path,
    #     server_type=server_type,
    #     server_id=server_id,
    #     http_handlers=Handler.http_path_methods)

    start_server(SdkServer,
                 SdkServer.init_server,
                 config_path="/GameConfig",
                 server_type='Sdk',
                 server_id=1,
                 port=10999,
                 http_handlers=Handler.http_path_methods)