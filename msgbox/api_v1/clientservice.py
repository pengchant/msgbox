"""
客户端的服务
"""

from flask import request, jsonify

from msgbox import db_session
from msgbox.api_v1 import api
from msgbox.models import User, SystemMessage
from msgbox.utils.common import json_param_required
from msgbox.utils.messge_util import get_usr_msg
from msgbox.utils.response_code import RET


@api.route("/client_update_msg", methods=['POST', 'GET'])
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

    if not all([workerid, msgslist]):
        return jsonify(re_code=RET.PARAMERR, msg="参数不完整")

    # 根据workerid查询用户的信息
    usr = User.query.filter(User.workerid == workerid).first()
    if usr is None:
        return jsonify(re_code=RET.PARAMERR, msg="工号非法")

    try:
        # 根据消息编号更新信息
        msg = SystemMessage.query.filter(SystemMessage.id.in_(tuple(msgslist))).update(
            {SystemMessage.msg_status: 'WAITTING_READ'})
        msg.status = "WAITTING_READ"
        db_session.commit()
        return jsonify(re_code=RET.OK, data=get_usr_msg(usr.id))
    except Exception as e:
        return jsonify(re_code=RET.DBERR, msg="查询数据失败，请稍后重试")
