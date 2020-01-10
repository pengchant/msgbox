"""后端应用通行证"""
from flask import render_template, request, jsonify, redirect, url_for, session

from msgbox.backendapp import bn
from msgbox.models import User
from msgbox.utils.response_code import RET


@bn.route("/login", methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        wkid = request.form.get("workerid")
        pwd = request.form.get("password")
        if not all([wkid, pwd]):  # 校验输入参数
            return jsonify(re_code=RET.PARAMERR, msg="参数错误")
        # 查询用户
        try:
            user = User.query.filter(User.workerid == wkid and User.usrrole == "ADMIN").first()
        except Exception as e:
            return jsonify(re_code=RET.DBERR, msg="数据库查询失败")
        # 如果用户不存在
        if not user:
            return jsonify(re_code=RET.NODATA, msg="用户不存在")
        # 判断是否为管理员
        if user.usrrole != 'ADMIN':
            return jsonify(re_code=RET.PARAMERR, msg="对不起您没有权限")
        # 校验密码
        if not user.check_password(pwd):
            return jsonify(re_code=RET.PARAMERR, msg="密码错误")

        session.clear()
        session['user_id'] = user.id
        session['user_name'] = user.real_name
        return jsonify(re_code=RET.OK, msg="登录成功")


@bn.route("/logout", methods=['POST', 'GET'])
def logout():
    """退出登录"""
    session.pop("user_id")
    session.pop("user_name")
    return jsonify(re_code=RET.OK, msg="退出成功")
