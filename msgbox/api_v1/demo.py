from flask import jsonify, request, render_template, url_for, session, redirect

from msgbox import redis_conn
from msgbox.api_v1 import api
from msgbox.auth.auth import JWTUtils
from msgbox.utils.common import token_required, login_required
from msgbox.utils.response_code import RET


@api.route('/sayhello', methods=['GET', 'POST'])
@token_required
def sayhello():
    """测试接口访问"""
    redis_conn.set("hello", "hahah")
    return jsonify(re_code=RET.OK, msg="你好，欢迎进入flask的世界!")


@api.route("/gettoken", methods=['GET', 'POST'])
def gettoken():
    """获取token"""
    dataobj = JWTUtils.encode_auth_token("1", "hahah")
    return jsonify(re_code=RET.OK, data=dataobj)


@api.route("/login", methods=['GET', 'POST'])
def login():
    """测试登录"""
    if request.method == 'GET':
        return render_template('auth/login1.html')
    else:
        user = request.form.get('username')
        # 存在session中
        session.clear()
        session['user_id'] = user
        return render_template("msbox/index.html", objdata={"usr": user})


@api.route("/loginout", methods=('GET',))
def logout():
    """测试退出登录"""
    session.clear()
    return redirect(url_for('api.login'))


@api.route("/toindex", methods=['GET'])
@login_required
def goindex():
    """查看首页"""
    return render_template("msbox/index.html", objdata={"usr": session.get("user_id")})
