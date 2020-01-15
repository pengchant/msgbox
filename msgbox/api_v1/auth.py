import time

from flask import request, jsonify

from msgbox.api_v1 import api
from msgbox.auth.auth import JWTUtils
from msgbox.models import User
from msgbox.utils.common import json_param_required
from msgbox.utils.response_code import RET


@api.route("/passport", methods=['POST'])
@json_param_required
def passport():
    """
    通行证
    :return:
    """
    jsonobj = request.json
    workerid = jsonobj.get("workerid")
    password = jsonobj.get("password")
    if not all([workerid, password]):
        return jsonify(re_code=RET.PARAMERR, msg="提交参数不完整")
    user = User.query.filter(User.workerid == workerid).first()
    if user is None:
        return jsonify(re_code=RET.PARAMERR, msg="该用户不存在")
    if not user.check_password(password):
        return jsonify(re_code=RET.PARAMERR, msg="密码错误")
    # 如果校验通过,生成token
    token = JWTUtils.encode_auth_token(user.workerid, str(time.time()))
    return jsonify(re_code=RET.OK, data=token, usr=user.to_dict())
