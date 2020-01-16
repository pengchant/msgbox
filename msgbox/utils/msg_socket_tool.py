import datetime

from msgbox.utils.redis_tool import CRedis


def setWorkeridSidMapper(sid, workerid):
    """
    设置sid和workerid 映射关系
    :param sid:
    :param workerid:
    :return:
    """
    try:
        conn = CRedis()
        key = "socketio:" + workerid
        conn.set(key, sid)
        conn.expire(key, datetime.timedelta(days=7))  # 设置七天后失效
        return True
    except Exception as e:
        return False


def getSIdByWorkerId(workerid):
    """
    根据workerid获取socket的sid
    :param workerid:
    :return:
    """
    conn = CRedis()
    return conn.get("socketio:" + workerid)
