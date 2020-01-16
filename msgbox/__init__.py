import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask, url_for, redirect
from flask_cors import CORS
from flask_session import Session

from msgbox import db, config, socketserver
from msgbox.config import APP_ENV
from .config import config
from .db import db_session

from .utils.common import login_required

redis_conn = None
session = Session()


def setupLogging(level):
    """创建日志记录"""
    logging.basicConfig(level=level)
    file_log_handler = RotatingFileHandler('/logs/log', maxBytes=1024 * 1024 * 100, backupCount=10)
    formatter = logging.Formatter('%(levelname)s %(filename)s: %(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)


def create_app():
    """创建一个app并配置这个app"""

    # 配置日志
    setupLogging(config[APP_ENV].LOGGINE_LEVEL)

    app = Flask(__name__)
    app.config.from_object(config[APP_ENV])

    # 跨域配置
    CORS(app, resources=r'/*')

    # 配置数据库
    db.init_app(app)

    # 配置redis
    global redis_conn
    redis_conn = redis.StrictRedis(host=config[APP_ENV].REDIS_HOST, port=config[APP_ENV].REDIS_PORT)

    # 配置session
    global session
    session.init_app(app)

    # 配置websocket
    socketserver.init_app(app)

    # 注册api_v1_0蓝图
    from msgbox.api_v1 import api
    app.register_blueprint(api)

    # 注册后端管理蓝图
    from msgbox.backendapp import bn
    app.register_blueprint(bn)

    @app.teardown_appcontext
    def shutdown_session(excetpion=None):
        """请求结束关闭连接"""
        db_session.remove()

    @app.route("/", methods=['GET'])
    @login_required
    def index():
        """进入后端首页"""
        return redirect(url_for('bn.gousrmanage'))

    return app
