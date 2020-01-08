"""客户端与服务器端socket通信模块"""
import logging
from random import random

from flask_socketio import send, SocketIO, emit

socketio = SocketIO()  # 基于flask_socketio实现服务器端与客户端的消息推送


def init_app(app):
    """初始化socket"""
    socketio.init_app(app)
    start_socket_server(app)


def start_socket_server(app):
    """开启socket服务器"""
    logging.info("开启socket服务器.端口5000")
    socketio.run(app=app, host="0.0.0.0", port=5000, debug=True)


@socketio.on('connect', namespace='/websocket/user_refresh')
def connect():
    """ 服务端自动发送通信请求 """
    emit('server_response', {'data': '试图连接客户端！'})


@socketio.on('connect_event', namespace='/websocket/user_refresh')
def refresh_message(message):
    """ 服务端接受客户端发送的通信请求 """
    emit('server_response', {'data': "请求成功"})


@socketio.on("receive_msg", namespace="/websocket/user_refresh")
def receive_msg(msg):
    """接收到来自客户端的消息"""
    strmsg = msg['data']
    emit("server_respchat", {'data': "你发送了：" + strmsg})
