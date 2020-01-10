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



