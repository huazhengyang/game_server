#! -*- coding:utf-8 -*-
# Time : 2020/12/24 3:31 下午 
# Author : borland83@126.com
# File : loginhandler.py 
# Comment: 
# Software: PyCharm

from gate import mark_http_handler
from gate import HttpHandler
from gate import log as rslog


@mark_http_handler(http_path='/open/v0/user/loginbydevid')
class UserLoginByDevID(HttpHandler):
    """
    请求方式：GET
    请求形式：https://xxx/open/v0/user/loginbydevid?appId=xxx&clientId=xxx&deviceName=xxx&devid=xxx
    """
    def check_params(self) -> bool:
        app_id = self.get_param('appId')
        client_id = self.get_param('clientId')
        device_name = self.get_param('deviceName')
        dev_id = self.get_param('devid')

        if None in (app_id, client_id, device_name, dev_id):
            rslog.error('user login paramter error')
            return False

        return True

    async def get(self) -> None:
        params_check = self.check_params()
        if not params_check:
            raise ValueError

        dev_id = self.get_param('devid')

        # 验证设备id是否已经注册
        # res = await MongoDBSchema.find(UserData.getUserCollection(), {'dev_id': dev_id})
        # if len(res) == 0:
        #     # todo 新用户, 生成user_id, 要求全球唯一
        #     pass
        # else:
        #     # todo app_id、client_id、device_name的验证暂时不做，还没想好
        #     pass

        self.write('ok')


    def post(self):
        pass

    def check_dev_id(self, dev_id):
        pass
