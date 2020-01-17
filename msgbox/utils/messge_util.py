import datetime
from sqlalchemy import and_, cast, DATE, or_

from msgbox.models import User, ServiceSystem, SystemMessage


def get_usr_msg(workerid):
    """
    根据用户的工号查询当前用户的所有的待阅读的消息
    1.未读消息，2.已读的【当天可继续查看】
    :param workerid:
    :return:
    """
    # 根据workerid查询用户的信息
    usr = User.query.filter(User.workerid == workerid).first()
    if usr is None:
        return None
    # 抓取所有的系统(OPENING)
    sys = ServiceSystem.query.filter(ServiceSystem.status == "OPENING").all()
    sys_dir = [v.to_sys_simple_dict() for v in sys]  # 所有开启的系统
    dat = datetime.date.today()
    msgs_q = SystemMessage.query.filter(SystemMessage.to_usr_id == usr.id,
                                        or_(SystemMessage.msg_status == 'WAITTING_READ',
                                            and_(SystemMessage.msg_status == "HAVE_READED",
                                                 cast(SystemMessage.msg_read_time, DATE) == dat)
                                            ))
    print(msgs_q)
    msgs = msgs_q.order_by(
        SystemMessage.msg_push_time.desc()).all()
    msgs_dir = [v.to_dict() for v in msgs]
    return {"sys": sys_dir, "msgs": msgs_dir}


def get_unsend_msg(workerid):
    """
    查看未曾发送的消息
    :param workerid:
    :return:
    """
    # 根据workerid查询用户的信息
    usr = User.query.filter(User.workerid == workerid).first()
    if usr is None:
        return None
    # 抓取所有的未发送的消息
    msgs = SystemMessage.query.filter(SystemMessage.msg_status == "WAITTING_SEND",
                                      SystemMessage.to_usr_id == usr.id).all()
    msgs_dir = [v.to_dict() for v in msgs]
    return msgs_dir
