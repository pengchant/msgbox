import logging

from redis import StrictRedis

APP_ENV = 'testing'


class BaseConfig:
    '''
    基础的配置
    '''
    # 避免返回中文为unicode字符
    JSON_AS_ASCII = False

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 是否开启跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "\xf9\x18<\x9b\xfd\xfc\xc20\xe5\x03b\xa8K7e\xe2q\xc7Z\x98\xf1\x15\x93\x91"

    # REDIS数据库的配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_DB = 1

    # 配置session数据存储到redis数据库
    SESSION_TYPE = 'redis'
    # 配置session的前缀
    SESSION_KEY_PREFIX = 'session:msgbox:'
    # 指定存储session的redis的位置
    SESSION_REIDS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    # 开启session数据的签名，让session数据不以明文的形式存储
    SESSION_USE_SIGNER = True
    # 配置session会话超时时长, 默认时间为1天
    PERMANENT_SESSION_LIFETIME = 3600 * 24


class TestingConfig(BaseConfig):
    '''测试环境'''
    DEBUG = True
    LOGGINE_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:root@localhost:3306/cssrcmsgbox?charset=utf8"


class DevelopmentConfig(BaseConfig):
    '''生产环境'''
    LOGGINE_LEVEL = logging.WARNING
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:root@localhost:3306/cssrcmsgbox?charset=utf8"


config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig
}
