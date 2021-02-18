#! -*- coding:utf-8 -*-
# Time : 2020/12/24 11:26 上午 
# Author : borland83@126.com
# File : userdata.py 
# Comment: 
# Software: PyCharm

from rainstorm.entity.exception import DBNotExistsException, DBCollectionNotExistsException
from rainstorm.entity.dao.daobase import DaoBase
from rainstorm.util import log as rslog

from common.entity.database.daoconst import RedisKey, SessionKey


class UserMGData(object):
    """
    mongodb的user信息操作，主要为用户信息
    """
    @classmethod
    def getUserCollection(cls):
        try:
            collection = DaoBase.get_collection('account', 'user')
        except DBNotExistsException:
            rslog.error('db account is not exists!, please check config file!')
        except DBCollectionNotExistsException:
            rslog.error('collection user is not exists!, please check config file!')
        except Exception as e:
            rslog.error('getUserCollection error!', e)

        else:
            return collection


class UserRDData(object):
    """
    redis的user信息操作，获取user库的连接并执行command
    """
    @classmethod
    async def run_user_cmd(cls, user_id, *cmd):
        """
        :param user_id:
        :return:
        """
        rslog.debug('run user cmd, user: {}, cmd: {}'.format(user_id, cmd))
        redis_conn = DaoBase.get_user_conn(user_id)
        if not redis_conn:
            raise DBNotExistsException('redis', str(user_id % DaoBase.redis_conn_user_len))

        return await redis_conn.execute_command(*cmd)


class UserSession(UserRDData):
    """
    操作用户的session数据
    """
    @classmethod
    def get_session_key(cls, user_id: int) -> str:
        return RedisKey.SESSION_DATA % user_id

    @classmethod
    async def set_session_single(cls, user_id, *cmd):
        key = cls.get_session_key(user_id)
        return await cls.run_user_cmd(user_id, 'hset', key, *cmd)

    @classmethod
    async def get_session_single(cls, user_id, *cmd):
        key = cls.get_session_key(user_id)
        return await cls.run_user_cmd(user_id, 'hget', key, *cmd)

    @classmethod
    async def set_session_multi(cls, user_id, *pairs):
        key = cls.get_session_key(user_id)
        return await cls.run_user_cmd(user_id, 'hmset', key, *pairs)

    @classmethod
    async def get_session_multi(cls, user_id, *keys):
        key = cls.get_session_key(user_id)
        return await cls.run_user_cmd(user_id, 'hmget', key, *keys)

    @classmethod
    async def get_session_without_scene(cls, user_id):
        key = cls.get_session_key(user_id)
        return await cls.run_user_cmd(user_id, 'hmget', key, SessionKey.SESSION_IP, SessionKey.SESSION_PORT,
                                      SessionKey.SESSION_GATE, SessionKey.SESSION_LAST_GAME,
                                      SessionKey.SESSION_ONLINE_STATE, SessionKey.SESSION_DEVICEID)


