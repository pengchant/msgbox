import hashlib
import time
from functools import wraps

from flask import session, jsonify, request, g, redirect, url_for

from msgbox.auth.auth import JWTUtils
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
    """生成appsecrect"""
    tempstr = val + str(time.time()) + secstr
    return sha256hex(tempstr)


def sha256hex(data):
    """sha256加密"""
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    res = sha256.hexdigest()
    return res
