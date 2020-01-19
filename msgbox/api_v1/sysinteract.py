"""第三方系统接入"""
import datetime
import re
import time

from flask import request, jsonify, render_template

from msgbox import db_session
from msgbox.api_v1 import api
from msgbox.auth.auth import JWTUtils
from msgbox.models import ServiceSystem, User, SystemMessage
from msgbox.utils.common import check_thirdpart_sys, token_required
from msgbox.utils.response_code import RET
from msgbox.socketserver import socketio, websocket_pushmsg


@api.route("/test", methods=["GET", "POST"])
def test():
    """测试推送消息"""
    return render_template("msbox/test.html")


@api.route("/testsocket", methods=["GET", "POST"])
def testsocket():
    """测试推送消息"""
    return render_template("msbox/testsocket.html")


@api.route("/getSignature", methods=["GET", "POST"])
@check_thirdpart_sys
def gettoken():
    """
    获取token
    :return:    token的json字符串
    """
    # 生成token
    appkey = request.args.get("appkey")
    token = JWTUtils.encode_auth_token(appkey, int(time.time()), timedela=datetime.timedelta(minutes=5))
    return jsonify(re_code=RET.OK, data=token)


@api.route("/pushmsg", methods=["GET", "POST"])
@token_required
def pushmsg():
    """
    推送消息:{tousr:'',url:'',des:''}
    0.校验所传递参数
    1.校验系统是否存在，并且为开启的状态
    2.校验用户是否存在
    3.将消息入库，并标记未读取（同时尝试推送客户端）
    :return:
    """
    appkey = request.args.get("appkey", None)
    jsonobj = request.json
    if not all([appkey, jsonobj]):
        return jsonify(re_code=RET.PARAMERR, msg="提交参数有误")
    touser = jsonobj.get("tousr")
    url = jsonobj.get("url")
    des = jsonobj.get("des")
    if not all([touser, url, des]):
        return jsonify(re_code=RET.PARAMERR, msg="参数不完整")
    # 验证url
    if not re.match(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", url):
        return jsonify(re_code=RET.PARAMERR, msg="url格式非法")
    # 校验系统
    sys = ServiceSystem.query.filter(ServiceSystem.appkey == appkey).first()
    if not sys or sys and sys.status == "CLOSED":
        return jsonify(re_code=RET.PARAMERR, msg="查无次系统")
    # 校验用户
    usr = User.query.filter(User.workerid == touser).first()
    if usr is None:
        return jsonify(re_code=RET.PARAMERR, msg="发送消息失败，该用户不存在，请联系管理员添加当前用户(工号):" + touser)
    # 消息入库
    msg = SystemMessage()
    msg.from_sys_id = sys.id
    msg.to_usr_id = usr.id
    msg.msg_title = des
    msg.msg_url = url
    msg.msg_status = "WAITTING_SEND"  # 待发送
    msg.msg_push_time = datetime.datetime.now()
    try:
        db_session.add(msg)
        db_session.commit()
        try:
            # todo:推送给客户端消息
            websocket_pushmsg({
                "msg_id": msg.id,
                "msg_title": msg.msg_title,
                "msg_url": msg.msg_url
            }, usr.workerid)
        except:
            # 默认继续处理
            pass
        return jsonify(re_code=RET.OK, msg="推送消息成功")
    except  Exception as e:
        return jsonify(re_code=RET.DBERR, msg="推送消息失败，请稍后重试")
