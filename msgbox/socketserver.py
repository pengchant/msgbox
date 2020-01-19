"""客户端与服务器端socket通信模块"""
import functools

import click
from flask import request, jsonify
from flask_socketio import emit, SocketIO

from msgbox.auth.auth import JWTUtils
from msgbox.utils.messge_util import get_unsend_msg
from msgbox.utils.msg_socket_tool import setWorkeridSidMapper, getSIdByWorkerId

socketio = SocketIO(cors_allowed_origins="*")  # 基于flask_socketio实现服务器端与客户端的消息推送


def init_app(app):
    """初始化socket"""
    socketio.init_app(app)
    start_socket_server(app)


def start_socket_server(app):
    """开启socket服务器"""
    click.echo("开启socket服务器.5000")
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
    emit('server_response', {'data': '*****试图连接服务器端*****'})


@socketio.on('disconnect', namespace="/websocket/usr_refresh")
def disconnect():
    """Connection Events 客户端失去连接"""
    click.echo("==== 客户端断开socket ====")


@socketio.on('connect_event', namespace='/websocket/user_refresh')
def refresh_message(message):
    """ 服务端接受客户端发送的通信请求 """
    # 将workerid->sid 的 映射放入redis缓存中
    sid = request.sid
    flag = setWorkeridSidMapper(sid, message.get("workerid"))
    if flag:
        # 当连接的时候就需要推送给用户信息[此时是消息列表]
        msglist = get_unsend_msg(message.get('workerid'))
        print(msglist)
        emit('init_response', {'data': msglist}, room=sid)
    else:
        emit("server_response", {'data': '请求失败'}, room=sid)


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


def websocket_pushmsg(data, workerid):
    """
    推送消息给客户端[此时是推送单个消息]
    :param data:
    :param workerid:
    :return:
    """
    sid = getSIdByWorkerId(workerid)
    if sid:
        roomid = str(sid, encoding="utf-8")
        socketio.emit("push_message", data, namespace="/websocket/user_refresh", room=roomid)
