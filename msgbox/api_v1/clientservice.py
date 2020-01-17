"""
客户端的服务
"""

from flask import request, jsonify

from msgbox import db_session
from msgbox.api_v1 import api
from msgbox.models import User, SystemMessage
from msgbox.utils.common import json_param_required, token_required
from msgbox.utils.messge_util import get_usr_msg
from msgbox.utils.response_code import RET


@api.route("/client_update_msg", methods=['POST', 'GET'])
@token_required
@json_param_required
def clientFetchData():
    """
    批量更新消息的状态，然后返回最新的消息
    :return:
    """
    # 获取工号和消息编号
    jsonobj = request.json
    workerid = jsonobj.get("workerid")
    msgslist = jsonobj.get("msgs")

    if workerid is None:
        return jsonify(re_code=RET.PARAMERR, msg="用户参数有误")

        # 根据workerid查询用户的信息
    usr = User.query.filter(User.workerid == workerid).first()
    if usr is None:
        return jsonify(re_code=RET.PARAMERR, msg="工号非法")

    try:
        if msgslist is not None and len(msgslist) > 0:
            # 根据消息编号更新信息
            msg_tuple = tuple(msgslist)
            SystemMessage.query.filter(SystemMessage.id.in_(msg_tuple)).update(
                {SystemMessage.msg_status: 'WAITTING_READ'},
                synchronize_session=False)
            db_session.commit()

        # 抓取所有的数据
        return jsonify(re_code=RET.OK, data=get_usr_msg(workerid))
    except Exception as e:
        print(e)
        return jsonify(re_code=RET.DBERR, msg="更新数据失败，请稍后重试")


@api.route("/update_hasread", methods=['POST', 'GET'])
@token_required
def update_hasread():
    """
    更新消息的状态已被阅读
    :return:
    """
    msgid = request.args.get("msgid")
    if not msgid:
        return jsonify(re_code=RET.PARAMERR, msg="提交参数有误")
    msg = SystemMessage.query.filter(SystemMessage.id == msgid).first()
    if msg is None:
        return jsonify(re_code=RET.PARAMERR, msg="查无消息")
    try:
        msg.msg_status = "HAVE_READED"
        db_session.commit()
        return jsonify(re_code=RET.OK, msg="修改消息状态成功")
    except Exception as e:
        return jsonify(re_code=RET.DBERR, msg="更新失败，请稍重试")
