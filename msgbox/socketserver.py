"""客户端与服务器端socket通信模块"""
import functools

import click
from flask import request
from flask_socketio import SocketIO, emit, join_room

from msgbox.auth.auth import JWTUtils

socketio = SocketIO(cors_allowed_origins="*")  # 基于flask_socketio实现服务器端与客户端的消息推送


def init_app(app):
    """初始化socket"""
    socketio.init_app(app)
    start_socket_server(app)


def start_socket_server(app):
    """开启socket服务器"""
    click.info("开启socket服务器.5000")
    socketio.run(app=app, host="0.0.0.0", port=5000)


def authenticated_only(f):
    """自定义授权方法"""

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        token = request.args.get("token")
        if token:
            result = JWTUtils.decode_auth_token(token)
            if result:
                return f(*args, **kwargs)

        return False

    return wrapped


@socketio.on('connect', namespace='/websocket/user_refresh')
# @authenticated_only
def connect():
    """ Connection Events 客户端发起通信请求 """
    click.echo("==== Connection Events 有客户端尝试连接socket  ====")
    emit('server_response', {'data': '试图连接服务器端！'})


@socketio.on('disconnect', namespace="/websocket/usr_refresh")
def disconnect():
    """Connection Events 客户端失去连接"""
    click.echo("==== 客户端断开socket ====")


@socketio.on('connect_event', namespace='/websocket/user_refresh')
def refresh_message(message):
    """ 服务端接受客户端发送的通信请求 """
    # todo：添加room
    print(message)
    emit('server_response', {'data': "请求成功"})


@socketio.on("receive_msg", namespace="/websocket/user_refresh")
def receive_msg(msg):
    """接收到来自客户端的消息"""
    strmsg = msg['data']
    emit("server_respchat", {'data': request.sid + ":" + strmsg}, broadcast=True)


def sendMsg(workerid, data):
    """给指定的用户发送消息"""


@socketio.on_error()
def error_handler(e):
    pass


@socketio.on_error('/chat')
def error_handler_chat(e):
    pass


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])  # "my error event"
    print(request.event["args"])
