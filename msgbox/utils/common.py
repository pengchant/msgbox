import base64
import datetime
import hashlib
import hmac
import time
from functools import wraps

from flask import session, jsonify, request, g, redirect, url_for

from msgbox.auth.auth import JWTUtils
from msgbox.models import ServiceSystem
from msgbox.utils.response_code import RET


def login_required(view):
    '''
    登录校验器
    :param handler:
    :param view_func:
    :return:
    '''

    @wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get("user_id")
        user_name = session.get("user_name")
        if not user_id:
            return redirect(url_for('bn.login'))
        else:
            g.user = {
                "user_id": user_id,
                "user_name": user_name
            }
            return view(**kwargs)

    return wrapped_view


def json_param_required(view):
    """
    json格式数据装饰器
    :param view:
    :return:
    """

    @wraps(view)
    def wrapped_view(**kwargs):
        jsonobj = request.json
        if jsonobj:
            return view(**kwargs)
        else:
            return jsonify(re_code=RET.PARAMERR, msg="请提交json格式数据")

    return wrapped_view


def token_required(view):
    """
    token校验器
    :param view:
    :return:
    """

    @wraps(view)
    def decorted(**kwargs):
        token = request.headers.get('Authorization', None)
        if token:
            result = JWTUtils.decode_auth_token(token)
            if result:
                return view(**kwargs)
        return jsonify(re_code=RET.SESSIONERR, msg="TOKEN校验失败")

    return decorted


def check_thirdpart_sys(view):
    """
    校验第三方系统请求头
    :param view:
    :return:
    """

    @wraps(view)
    def decorted(**kwargs):
        # 校验请求头
        appkey = request.args.get("appkey")
        timestap = request.headers["timestap"]
        accesstoken = request.headers["accesstoken"]
        signature = request.headers["signature"]
        # 判断空
        if not all([appkey, timestap, accesstoken, signature]):
            return jsonify(re_code=RET.PARAMERR, msg="请求参数不完全")
        # 校验appkey是否和请求中的accesstoken一致
        if appkey != accesstoken:
            return jsonify(re_code=RET.PARAMERR, msg="请求参数有误")
        # 校验时间戳是否过时
        if not before5min(float(timestap)):
            return jsonify(re_code=RET.PARAMERR, msg="超时请重试")
        # 查询应用
        sys = ServiceSystem.query.filter(ServiceSystem.appkey == appkey).first()
        if sys is None:
            return jsonify(re_code=RET.PARAMERR, msg="此系统不存在")
        # 校验是否开启
        if sys.status == "CLOSED":
            return jsonify(re_code=RET.PARAMERR, msg="系统已关闭请联系管理员")
            # 验证参数
        url = "/api/v1.0/getSignature?appkey=" + appkey + " " + timestap
        sign = str(base64.b64encode(generateSign(sys.appsecrect, url).encode('utf-8')), 'utf-8')
        if sign != signature:
            return jsonify(re_code=RET.PARAMERR, msg="签名验证非法")

        return view(**kwargs)

    return decorted


def page_helper_getparam(request):
    """
    从request请求头中获取分页的相关参数
    :param request:
    :return:
    """
    filterobj = request.json
    if filterobj is None:
        return None
    page = filterobj.get('page')
    if page == 0:
        page = 1
    pagesize = filterobj.get('pagesize')
    condition = filterobj.get('condition')
    if not all([page, pagesize, condition]):
        return None
    return {
        "page": page,
        "pagesize": pagesize,
        "condition": condition
    }


def page_helper_filter(querydata, filterobj, handler=None):
    """
    分页查询
    :param querydata:
    :param filterobj:
    :param handler: 结果处理器
    :return:{page:1, size:10, pages:4, total:56, data:[]} | {}
    """
    try:
        total = querydata.count()
        pages = int((total + filterobj['pagesize'] - 1) / filterobj['pagesize'])
        pagedData = querydata.limit(filterobj['pagesize']).offset((filterobj['page'] - 1) * filterobj['pagesize'])
        if handler is not None:
            pagedData = handler(pagedData)
    except Exception as e:
        return None
    return {
        "page": filterobj['page'],
        "size": filterobj['pagesize'],
        'pages': pages,
        "total": total,
        "data": pagedData
    }


def generate_secrectkey(val, secstr):
    """
    生成appsecrect
    :param val:
    :param secstr:
    :return:
    """
    tempstr = val + str(time.time()) + secstr
    return sha256hex(tempstr)


def sha256hex(data):
    """
    sha256加密
    :param data:
    :return:
    """
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    res = sha256.hexdigest()
    return res


def before5min(time_stmp):
    """
    验证时间戳是否为5min之内
    :param time_stmp:
    :return:
    """
    try:
        t = datetime.datetime.now()
        t1 = t.strftime("%Y-%m-%d %H:%M:%S")
        ts1 = time.mktime(time.strptime(t1, "%Y-%m-%d %H:%M:%S"))
        t2 = (t - datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        ts2 = time.mktime(time.strptime(t2, "%Y-%m-%d %H:%M:%S"))
        return time_stmp >= ts2
    except Exception as e:
        return False


def generateSign(appkey, strtoSign):
    """
    生成签名
    :param appkey:
    :param strtoSign:
    :return:
    """
    signature = hmac.new(bytes(appkey, encoding='utf-8'), bytes(strtoSign, encoding='utf-8'),
                         digestmod=hashlib.sha256).digest()
    HEX = signature.hex()
    lowsigne = HEX.lower()
    return lowsigne
