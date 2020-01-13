"""后端应用通行证"""
from flask import render_template, request, jsonify, redirect, url_for, session

from msgbox import login_required, db_session
from msgbox.backendapp import bn
from msgbox.models import User
from msgbox.utils.response_code import RET


@bn.route("/login", methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        # 参数空判断
        wkid = request.form.get("workerid")
        pwd = request.form.get("password")
        if not all([wkid, pwd]):  # 校验输入参数
            return jsonify(re_code=RET.PARAMERR, msg="参数错误")

        # 查询用户
        try:
            user = User.query.filter(User.workerid == wkid and User.usrrole == "ADMIN").first()
        except Exception as e:
            return jsonify(re_code=RET.DBERR, msg="数据库查询失败")

        # 判断用户是否存在
        if not user:
            return jsonify(re_code=RET.NODATA, msg="用户不存在")

        # 校验密码
        if not user.check_password(pwd):
            return jsonify(re_code=RET.PARAMERR, msg="密码错误")

        # 判断是否为管理员
        if user.usrrole != 'ADMIN':
            return jsonify(re_code=RET.PARAMERR, msg="对不起您没有权限")

        session.clear()
        session['user_id'] = user.id
        session['user_name'] = user.real_name
        return jsonify(re_code=RET.OK, msg="登录成功")


@bn.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    """退出登录"""
    session.pop("user_id")
    session.pop("user_name")
    return jsonify(re_code=RET.OK, msg="退出成功")


@bn.route("/changepwd", methods=['GET', 'POST'])
@login_required
def changepwd():
    """修改密码"""
    usrid = session.get("user_id")
    oldpwd = request.form.get("oripass")
    newpwd = request.form.get("newpass")
    surepwd = request.form.get("surepass")

    if not all([newpwd, surepwd]):
        return jsonify(re_code=RET.PARAMERR, msg="参数不完整")

    if newpwd != surepwd:
        return jsonify(re_code=RET.PARAMERR, msg="两次密码输入不一致")

    try:
        u = User.query.filter(User.id == usrid).first()
        if not u.check_password(oldpwd):
            return jsonify(re_code=RET.PARAMERR, msg="旧密码错误")

        if u.check_password(newpwd):
            return jsonify(re_code=RET.PARAMERR, msg="新密码不能与现有的密码重复")

        u.password_hash = newpwd
        db_session.commit()
        session.pop("user_id")
        session.pop("user_name")
        return jsonify(re_code=RET.OK, msg="修改密码成功,请重新登录")
    except Exception as e:
        return jsonify(re_code=RET.DBERR, msg="修改密码失败,请稍后重试")
