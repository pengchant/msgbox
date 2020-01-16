"""
客户端的服务
"""
from datetime import datetime

from flask import request, jsonify
from sqlalchemy import or_, and_, cast, DATE

from msgbox.api_v1 import api
from msgbox.models import ServiceSystem, User, SystemMessage
from msgbox.utils.response_code import RET


@api("/client-fetch", methods=['POST', 'GET'])
def clientFetchData():
    """
    抓取data
    :return:
    """
    workerid = request.args.get("workerid")
    if not workerid:
        return jsonify(re_code=RET.PARAMERR, msg="工号不能为空")
    # 根据workerid查询用户的信息
    usr = User.query.filter(User.workerid == workerid).first()
    if usr is None:
        return jsonify(re_code=RET.PARAMERR, msg="工号非法")
    try:
        # 抓取所有的系统(OPENING)
        sys = ServiceSystem.query.filter(ServiceSystem.status == "OPENING").all()
        sys_dir = [v.to_sys_simple_dict() for v in sys]  # 所有开启的系统
        # 抓取所有的未读的消息(1.未读消息，2.已读的【当天可继续查看】)
        dat = datetime.date.today()
        msgs = SystemMessage.query.filter(or_(
            and_(SystemMessage.to_usr_id == usr.id,
                 SystemMessage.msg_status == 'WAITTING_READ'),
            and_(SystemMessage.msg_status == "HAVE_READED",
                 cast(SystemMessage.msg_read_time, DATE) == dat)
        )).all()
        msgs_dir = [v.to_dict() for v in msgs]
        return jsonify(re_code=RET.OK, data={"sys": sys_dir, "msg": msgs_dir})
    except Exception as e:
        return jsonify(re_code=RET.DBERR, msg="查询数据失败，请稍后重试")
