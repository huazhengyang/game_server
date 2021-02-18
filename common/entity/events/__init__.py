#! -*- coding:utf-8 -*-
# Time : 2021/2/5 6:09 下午 
# Author : borland83@126.com
# File : __init__.py 
# Comment: 
# Software: PyCharm

from rainstorm.entity.event.event import UserEvent


class UserSecneChangeEvent(UserEvent):
    def __init__(self, user_id, game_id, scene_id):
        super(UserSecneChangeEvent, self).__init__(user_id, game_id)
        self._scene_id = scene_id

    @property
    def scene_id(self):
        return self._scene_id
